#!/usr/bin/env python3
"""VibeCoder DevKit 2 — instalação portátil, idempotente, auditável e reversível.

Por padrão: sem alterações e sem rede. Instalações externas só com --apply e flags
explícitas. O instalador não lê nem imprime segredos, tokens ou conteúdo de projetos.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import tomllib
from contextlib import contextmanager

ROOT = Path(__file__).resolve().parents[1]
PROFILES = ('core', 'web', 'security', 'full')
START = '<!-- vibecoder-devkit:begin -->'
END = '<!-- vibecoder-devkit:end -->'
STATE_NAME = 'devkit-state.json'
VERSION = '2.0.0'


class DevKitError(Exception):
    pass


def load_json(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha_file(path):
    return sha_bytes(path.read_bytes())


def home_codex():
    return Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))).expanduser().resolve()


def get_paths(args):
    if args.scope == 'global':
        root = home_codex()
        return root, root / 'agents', Path.home() / '.agents' / 'skills', root / 'AGENTS.md'
    project = Path(args.target or '.').expanduser().resolve()
    return project / '.codex', project / '.codex' / 'agents', project / '.agents' / 'skills', project / 'AGENTS.md'


def ensure_safe_target(path, allowed_roots):
    """Recusa destino symlink (inclusive ancestrais abaixo das raízes)."""
    path = Path(path)
    if not any(path == root or root in path.parents for root in allowed_roots):
        raise DevKitError('Destino fora das raízes autorizadas do DevKit')
    for part in (path, *path.parents):
        if part.is_symlink():
            raise DevKitError(f'Symlink no destino; revisão manual obrigatória: {part}')
        if part in allowed_roots:
            break


def stamp():
    return dt.datetime.now().strftime('%Y%m%d-%H%M%S-%f')


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.' + path.name + '.', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def read_bytes(path):
    return path.read_bytes() if path.is_file() else None


def rendered_rules(path, source):
    excerpt = source.read_text(encoding='utf-8').strip()
    original = path.read_text(encoding='utf-8-sig') if path.exists() else ''
    if (START in original) != (END in original):
        raise DevKitError('Marcadores AGENTS.md incompletos; revisão manual necessária')
    addition = START + '\n' + excerpt + '\n' + END
    if START in original:
        if original.count(START) != 1 or original.count(END) != 1:
            raise DevKitError('Marcadores AGENTS.md duplicados; revisão manual necessária')
        new = original[:original.index(START)] + addition + original[original.index(END)+len(END):]
    else:
        new = original.rstrip() + ('\n\n' if original.strip() else '') + addition + '\n'
    return new.encode('utf-8')


def render_config(path, max_agents):
    content = path.read_text(encoding='utf-8-sig') if path.exists() else ''
    try:
        obj = tomllib.loads(content) if content.strip() else {}
    except tomllib.TOMLDecodeError as e:
        raise DevKitError(f'config.toml inválido (não alterado): {e}') from e
    settings = obj.get('agents', {})
    if not isinstance(settings, dict):
        raise DevKitError('A seção [agents] precisa ser tabela TOML')
    missing = {}
    if 'enabled' not in settings:
        missing['enabled'] = True
    if 'max_concurrent_threads_per_session' not in settings and 'max_threads' not in settings:
        missing['max_concurrent_threads_per_session'] = max_agents
    if not missing:
        return content.encode('utf-8'), ()
    additions = ''.join(f'{k} = {str(v).lower() if isinstance(v, bool) else v}\n' for k, v in missing.items())
    heads = list(re.finditer(r'(?m)^\s*\[([^\]\n]+)\]\s*$', content))
    section = next((h for h in heads if h.group(1).strip() == 'agents'), None)
    if section:
        updated = content[:section.end()] + '\n' + additions + content[section.end():]
    else:
        updated = content.rstrip('\r\n') + '\n\n[agents]\n' + additions
    tomllib.loads(updated)
    return updated.encode('utf-8'), tuple(missing)


def listed_agents(profile):
    data = load_json('catalog/agents.json')
    allowed = {a['id'] for a in data['agents'] if profile in a['profiles']}
    source = {f.stem: f for f in (ROOT / 'agents').glob('*.toml')}
    unknown = allowed - source.keys()
    if unknown:
        raise DevKitError('Agentes no catálogo não encontrados: ' + ', '.join(sorted(unknown)))
    return [source[k] for k in sorted(allowed)]


def selected_skills(profile):
    cat = load_json('catalog/skills.json')['skills']
    return [s for s in cat if profile in s['profiles']]


def selected_tools(profile):
    return [t for t in load_json('catalog/tools.json')['tools'] if profile in t['profiles']]


def check_catalog():
    roles = load_json('catalog/agents.json')['agents']
    role_ids = [r['id'] for r in roles]
    assert len(role_ids) == len(set(role_ids)), 'IDs de agente duplicados'
    assert set(role_ids) == {f.stem for f in (ROOT/'agents').glob('*.toml')}, 'Agentes fora do catálogo'
    for role in roles:
        assert set(role['profiles']).issubset(PROFILES), role
        toml = tomllib.loads((ROOT/'agents'/f"{role['id']}.toml").read_text(encoding='utf-8'))
        assert toml['name'] == role['id']
    entries = load_json('catalog/skills.json')['skills']
    pairs = [(e['repo'], e['name']) for e in entries]
    assert len(pairs) == len(set(pairs)), 'Skill duplicada'
    for e in entries:
        assert e['source'].startswith('https://'), e
        assert set(e['profiles']).issubset(PROFILES), e
    for e in load_json('catalog/tools.json')['tools']:
        assert set(e['profiles']).issubset(PROFILES), e


def command_text(argv):
    return subprocess.list2cmdline(argv) if os.name == 'nt' else shlex.join(argv)


def invoke(argv, apply=False, failures=None, cwd=None):
    print('  $ ' + command_text(argv))
    if not apply:
        return True
    if shutil.which(argv[0]) is None:
        print('    PENDENTE: executável não encontrado')
        if failures is not None: failures.append(argv[0] + ': ausente')
        return False
    try:
        result = subprocess.run(argv, cwd=cwd, capture_output=True, text=True,
                                errors='replace', timeout=420)
        # Não imprime saída integral de CLIs de terceiros: pode conter tokens/URLs privados.
        print('    resultado:', 'OK' if result.returncode == 0 else f'falhou ({result.returncode})')
        if result.returncode and failures is not None:
            failures.append(argv[0] + ': retorno não-zero')
        return result.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        print('    PENDENTE: erro ou timeout do comando externo')
        if failures is not None: failures.append(argv[0] + ': erro/timeout')
        return False


def node_version():
    node = shutil.which('node')
    if not node: return None
    try:
        value = subprocess.check_output([node, '--version'], timeout=5, text=True).strip()
        match = re.match(r'v?(\d+)\.(\d+)', value)
        return (int(match.group(1)), int(match.group(2))) if match else None
    except (OSError, subprocess.SubprocessError):
        return None


def node_sufficient():
    return bool(node_version() and node_version() >= (22, 20))


def npx():
    return 'npx.cmd' if os.name == 'nt' else 'npx'


def npm():
    return 'npm.cmd' if os.name == 'nt' else 'npm'


def check_requirements(args):
    """Nenhum arquivo local será modificado antes da validação completa."""
    check_catalog()
    base, agents, skills, rules = get_paths(args)
    allowed = (base, agents, skills, rules.parent)
    for dest in (base/'config.toml', base/STATE_NAME, rules, agents, skills):
        ensure_safe_target(dest, allowed)
    render_config(base/'config.toml', args.max_agents)
    rendered_rules(rules, ROOT/'templates'/('AGENTS.global.md' if args.scope=='global' else 'AGENTS.project.md'))
    for src in listed_agents(args.profile):
        ensure_safe_target(agents/src.name, allowed)
    for src in sorted((ROOT/'.agents/skills').glob('*/**/*')):
        if src.is_symlink(): raise DevKitError('Não são permitidos symlinks em skills locais: '+src.name)
        if src.is_file():
            ensure_safe_target(skills/src.relative_to(ROOT/'.agents/skills'), allowed)
    if args.with_skills and args.apply and not node_sufficient():
        raise DevKitError('Para instalar skills externas, instale Node >=22.20 e npx')
    if args.with_design and args.apply and (node_version() is None or node_version() < (18, 19)):
        raise DevKitError('Para instalar Impeccable, instale Node >=18.19')
    if args.with_skills and args.apply and not shutil.which('git'):
        raise DevKitError('Git é necessário para baixar as skills de terceiros')
    if (args.with_skills or args.with_design) and args.apply and not shutil.which(npx()):
        raise DevKitError('npx ausente no PATH')
    return base, agents, skills, rules


@contextmanager
def session_lock(base):
    lock = base / '.devkit-install.lock'
    base.mkdir(parents=True, exist_ok=True)
    try:
        handle = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as err:
        raise DevKitError('Instalação concorrente detectada; verifique/remova lock órfão manualmente') from err
    try:
        with os.fdopen(handle,'w') as fp:
            fp.write('VibeCoder DevKit install lock\n')
        yield
    finally:
        lock.unlink(missing_ok=True)


class ManagedFiles:
    """Registra alterações locais; jamais modifica arquivo não pertencente ao DevKit."""
    def __init__(self, base, agents, skills, rules, apply):
        self.base, self.agents, self.skills, self.rules, self.apply = base, agents, skills, rules, apply
        self.state_file = base / STATE_NAME
        self.old = json.loads(self.state_file.read_text(encoding='utf-8')) if self.state_file.exists() else {'version':VERSION,'managed':{}}
        self.managed = dict(self.old.get('managed', {}))
        self.backup = base/'devkit-backups'/stamp()
        self.journal=[]
        self.changes=0
        self.skips=[]

    def permitted(self, dest):
        allowed = (self.base, self.agents, self.skills, self.rules.parent)
        ensure_safe_target(dest, allowed)
        # Manifest entries may refer ONLY to configured Codex targets.
        if dest in (self.base/'config.toml',self.rules): return
        if dest.parent == self.agents and dest.suffix == '.toml': return
        if self.skills in dest.parents and len(dest.relative_to(self.skills).parts) >= 2: return
        raise DevKitError('Caminho do manifesto não autorizado')

    def put(self, dest, data, label='arquivo', allow_unowned=False):
        dest = Path(dest)
        self.permitted(dest)
        key = str(dest)
        before = read_bytes(dest)
        digest = sha_bytes(data)
        existing = self.managed.get(key)
        if before is not None and existing is not None and sha_bytes(before) != existing.get('sha256'):
            self.skips.append(str(dest))
            print(f'  PRESERVADO {label} {dest.name} (modificado pelo usuário após instalar)')
            return
        if before == data:
            print(f'  OK {label} {dest.name} (já atualizado)')
            return
        if before is not None and ((existing is None and not allow_unowned) or (existing is not None and sha_bytes(before) != existing.get('sha256'))):
            self.skips.append(str(dest))
            print(f'  PRESERVADO {label} {dest.name} (arquivo existente ou modificado pelo usuário)')
            return
        action = 'CRIAR' if before is None else 'ATUALIZAR'
        print(f'  {action} {label} {dest.name}')
        if not self.apply: return
        previous = existing or {'origin':'created' if before is None else 'replaced'}
        origin = previous['origin']
        saved_backup = previous.get('backup')
        if origin == 'replaced' and saved_backup is None and before is not None:
            self.backup.mkdir(parents=True, exist_ok=True)
            target = self.backup/(hashlib.sha256(key.encode()).hexdigest()[:16]+'.bak')
            target.write_bytes(before)
            saved_backup = str(target)
        self.journal.append((dest, before))
        atomic_write(dest, data)
        self.managed[key] = {'sha256': digest, 'origin': origin, 'backup': saved_backup}
        self.changes += 1

    def save(self):
        if not self.apply: return
        data = json.dumps({'version':VERSION,'managed':self.managed}, indent=2, sort_keys=True, ensure_ascii=False).encode('utf-8') + b'\n'
        self.journal.append((self.state_file, read_bytes(self.state_file)))
        atomic_write(self.state_file, data)

    def undo_on_error(self):
        for path, before in reversed(self.journal):
            if before is None: path.unlink(missing_ok=True)
            else: atomic_write(path, before)


def local_install(args, mgr):
    for src in listed_agents(args.profile):
        mgr.put(mgr.agents/src.name,src.read_bytes(),'agente')
    for path in sorted((ROOT/'.agents/skills').glob('*/**/*')):
        if path.is_file():
            target=mgr.skills/path.relative_to(ROOT/'.agents/skills')
            mgr.put(target,path.read_bytes(),'skill')
    config = mgr.base/'config.toml'
    updated, keys = render_config(config,args.max_agents)
    if keys: print('  config.toml: acrescentar', ', '.join(keys))
    mgr.put(config,updated,'configuração',allow_unowned=True)
    source = ROOT/'templates'/('AGENTS.global.md' if args.scope=='global' else 'AGENTS.project.md')
    mgr.put(mgr.rules,rendered_rules(mgr.rules,source),'regras',allow_unowned=True)
    if (mgr.base/'AGENTS.override.md').exists():
        print('  AVISO: AGENTS.override.md pode ter precedência sobre regras globais.')


def third_party_skills(args, failures):
    grouped={}
    for entry in selected_skills(args.profile):
        grouped.setdefault(entry['repo'], []).append(entry['name'])
    print(f'\n[Skills externas] {sum(map(len,grouped.values()))} skills, {len(grouped)} fornecedores')
    for repo,names in sorted(grouped.items()):
        cli_version=load_json('catalog/versions.json')['npm']['skills']
        command=[npx(),'-y','skills@'+cli_version,'add',repo]
        for name in names: command += ['--skill',name]
        command += ['-a','codex']
        if args.scope=='global':command += ['-g']
        command += ['-y']
        invoke(command,apply=args.apply,failures=failures,cwd=args.target or str(ROOT))


def design_install(args, failures):
    print('\n[Impeccable] Sem hooks automáticos')
    impeccable_version=load_json('catalog/versions.json')['npm']['impeccable']
    cmd=[npx(),'-y','impeccable@'+impeccable_version,'install','--providers=codex',
         '--scope='+('global' if args.scope=='global' else 'project'),'--no-hooks']
    invoke(cmd,apply=args.apply,failures=failures,cwd=args.target or str(ROOT))


def install_one_tool(tool, failures, *, apply):
    if shutil.which(tool['probe']):
        print(f'  PRESENTE {tool["id"]}'); return
    system=platform.system()
    if 'npm_package' in tool:
        invoke([npm(),'install','-g',tool['npm_package']],apply=apply,failures=failures)
    elif system=='Windows' and 'windows_winget' in tool:
        invoke(['winget','install','-e','--id',tool['windows_winget'],
                '--accept-source-agreements','--accept-package-agreements'],apply=apply,failures=failures)
    elif system in ('Darwin','Linux') and shutil.which('brew') and 'mac_linux_brew' in tool:
        invoke(['brew','install',tool['mac_linux_brew']],apply=apply,failures=failures)
    elif tool['id']=='semgrep' and shutil.which('uv'):
        invoke(['uv','tool','install','semgrep'],apply=apply,failures=failures)
    else:
        print('  MANUAL',tool['id'],tool['source'])
        if apply: failures.append(tool['id']+': instalar manualmente')


def third_party_tools(args, failures):
    print('\n[CLIs externas]')
    for tool in selected_tools(args.profile):
        install_one_tool(tool,failures,apply=args.apply)


def install_rtk_hook(args, failures, mgr):
    if args.scope != 'global':
        print('  RTK hook global: use --scope global');return
    print('\n[RTK] Prévia do hook')
    if not shutil.which('rtk'):
        print('  PENDENTE: RTK não encontrado; instale primeiro a CLI')
        if args.apply: failures.append('RTK ausente no PATH')
        return
    invoke(['rtk','init','-g','--codex','--dry-run'],apply=args.apply,failures=failures)
    if args.apply:
        for item in ('hooks.json','AGENTS.md','RTK.md'):
            path = mgr.base/item
            if path.is_file():
                mgr.backup.mkdir(parents=True,exist_ok=True)
                shutil.copy2(path,mgr.backup/('rtk-'+item))
        invoke(['rtk','init','-g','--codex'],apply=True,failures=failures)
        print('  Hook gerenciado pelo RTK; reversão: rtk init -g --codex --uninstall')


def doctor(as_json=False):
    binaries=['python','python3','git','node','npx','codex','rtk','playwright-cli','semgrep','gitleaks','uv','winget','brew']
    result={'devkit':VERSION,'python':platform.python_version(),'platform':platform.system(),
            'codex_home':str(home_codex()),'node_22_20_or_newer':node_sufficient(),
            'commands':{x: bool(shutil.which(x)) for x in binaries}}
    if as_json: print(json.dumps(result,indent=2,ensure_ascii=False));return
    print(f'VibeCoder DevKit {VERSION} | Python {result["python"]} | {result["platform"]}')
    print('Node >=22.20:',result['node_22_20_or_newer'])
    for k,v in result['commands'].items():print(f'  {k:16s} {"OK" if v else "ausente"}')


def audit(args):
    base,agents,skills,rules=get_paths(args)
    state=base/STATE_NAME
    if not state.is_file():
        print('Nenhuma instalação local gerenciada registrada neste escopo.');return 1
    mgr=ManagedFiles(base,agents,skills,rules,False)
    records=[]
    for raw,entry in sorted(mgr.managed.items()):
        p=Path(raw)
        try: mgr.permitted(p)
        except DevKitError: status='INVALIDO'
        else: status=('OK' if p.is_file() and sha_file(p)==entry['sha256']
                      else 'MODIFICADO' if p.exists() else 'AUSENTE')
        records.append({'file':raw,'status':status})
    if args.json: print(json.dumps({'version':VERSION,'files':records},indent=2,ensure_ascii=False))
    else:
        for v in records:print(f'  {v["status"]:10s} {v["file"]}')
        print(f'Auditados: {len(records)}; atenção: apenas arquivos gerenciados localmente; não valida Codex em execução.')
    return 0 if all(r['status']=='OK' for r in records) else 1


def uninstall(args):
    base,agents,skills,rules=get_paths(args)
    state=base/STATE_NAME
    if not state.exists():
        print('Nenhum manifesto encontrado; nada a remover.');return 0
    mgr=ManagedFiles(base,agents,skills,rules,args.apply)
    changes=[]
    for raw,entry in sorted(mgr.managed.items()):
        p=Path(raw)
        mgr.permitted(p)
        if not p.is_file() or sha_file(p)!=entry['sha256']:
            print('  PRESERVADO (modificado/ausente)',p.name);continue
        original=None
        if entry.get('origin')=='replaced':
            backup=Path(entry.get('backup') or '')
            if not backup.is_file() or backup.is_symlink() or not (mgr.base/'devkit-backups') in backup.parents or any(part.is_symlink() for part in backup.parents if part != mgr.base):
                print('  PRESERVADO (backup não verificado)',p.name);continue
            original=backup.read_bytes()
        print('  RESTAURAR' if original is not None else '  REMOVER',p.name)
        changes.append((p,original))
    if not args.apply:
        print('Prévia apenas; use uninstall --apply para executar.')
        return 0
    with session_lock(base):
        for p, original in changes:
            if original is None:p.unlink(missing_ok=True)
            else:atomic_write(p,original)
        # Conserva manifesto quando algo foi modificado e não pode ser removido.
        remaining={str(p):entry for p_str,entry in mgr.managed.items() for p in [Path(p_str)]
                   if p.is_file() and sha_file(p)==entry['sha256']}
        if remaining:
            atomic_write(state,json.dumps({'version':VERSION,'managed':remaining},indent=2).encode('utf-8'))
            print('Itens não removidos ainda constam no manifesto.')
        else:state.unlink(missing_ok=True)
    print('Concluído. Dependências e hooks externos não foram removidos automaticamente.')
    return 0


def install(args):
    base,agents,skills,rules = check_requirements(args)
    print(f'Perfil={args.profile} | escopo={args.scope} | modo={"APLICAR" if args.apply else "PRÉVIA"}')
    print(f'Agentes selecionados={len(listed_agents(args.profile))} | skills externas={len(selected_skills(args.profile))} | CLIs={len(selected_tools(args.profile))}')
    failures=[]

    def perform():
        mgr=ManagedFiles(base,agents,skills,rules,args.apply)
        try:
            local_install(args,mgr)
            mgr.save()
        except Exception:
            mgr.undo_on_error()
            raise
        print('  Arquivos locais modificados:',mgr.changes,'| conflitos preservados:',len(mgr.skips))
        if args.with_skills:third_party_skills(args,failures)
        if args.with_design and args.profile in ('web','full'):design_install(args,failures)
        if args.with_tools:third_party_tools(args,failures)
        if args.with_rtk_hook:install_rtk_hook(args,failures,mgr)
        return mgr

    if args.apply:
        with session_lock(base):mgr=perform()
    else:mgr=perform()
    if failures:
        print('Pendências externas (instalação local preservada):')
        for f in failures:print('  -',f)
    print('Valide a descoberta dos agentes no Codex após reiniciar. Nenhuma economia de 90% é garantida.')
    return 1 if failures or mgr.skips else 0


def main(argv=None):
    if sys.version_info < (3,11):
        print('Python 3.11+ é obrigatório.',file=sys.stderr);return 2
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='cmd',required=True)
    p=sub.add_parser('doctor');p.add_argument('--json',action='store_true')
    for command in ('plan','install','audit','uninstall'):
        p=sub.add_parser(command)
        p.add_argument('--scope',choices=('global','project'),default='global')
        p.add_argument('--target',help='Diretório raiz do projeto')
        if command in ('plan','install'):
            p.add_argument('--profile',choices=PROFILES,default='core')
            p.add_argument('--max-agents',type=int,choices=range(1,9),metavar='1..8',default=3)
            p.add_argument('--apply',action='store_true')
            p.add_argument('--with-skills',action='store_true')
            p.add_argument('--with-design',action='store_true')
            p.add_argument('--with-tools',action='store_true')
            p.add_argument('--with-rtk-hook',action='store_true')
        elif command=='audit':p.add_argument('--json',action='store_true')
        else:p.add_argument('--apply',action='store_true')
    args=parser.parse_args(argv)
    if args.cmd=='plan' and args.apply:parser.error('plan não aceita --apply')
    try:
        if args.cmd=='doctor':doctor(args.json);return 0
        if args.cmd in ('plan','install'):return install(args)
        if args.cmd=='audit':return audit(args)
        if args.cmd=='uninstall':return uninstall(args)
    except (OSError,ValueError,DevKitError,KeyError,AssertionError) as e:
        # não exibir caminhos/dados de credenciais vindos de programas externos.
        print('ERRO:',str(e)[:320],file=sys.stderr);return 1
    return 2


if __name__=='__main__':sys.exit(main())
