#!/usr/bin/env python3
"""Especialidades VibeCoder: instalação segura, modular e auditável de skills para Codex.

Nenhum download/alteração em plan, list ou recommend. Para mudar a máquina,
use install --apply; para instalar terceiros, acrescente --with-external.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'catalog' / 'specialty-packs.json'
STATE = 'devkit-specialty-state.json'


def catalog():
    return json.loads(CATALOG.read_text(encoding='utf-8'))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def paths(args):
    if args.scope == 'global':
        base = Path(os.environ.get('CODEX_HOME', Path.home()/'.codex')).expanduser().resolve()
        skills = Path.home()/'.agents'/'skills'
    else:
        target=Path(args.target or '.').expanduser().resolve()
        base=target/'.codex'
        skills=target/'.agents'/'skills'
    return base,skills


def require_safe(path, root):
    path=Path(path)
    root=Path(root)
    if path != root and root not in path.parents:
        raise ValueError(f'caminho fora do diretório autorizado: {path.name}')
    for part in (path,*path.parents):
        if part.is_symlink():
            raise ValueError(f'symlink em destino: {part.name}')
        if part==root:break


def validate_catalog():
    c=catalog()
    packs={p['id']:p for p in c['packs']}
    assert len(packs)==len(c['packs']) and c['schema']==3
    local=ROOT/'specialties'/'skills'
    installed=set()
    for p in packs.values():
        assert p['local_skills'] or p['external_skills']
        for name in p['local_skills']:
            f=local/name/'SKILL.md'
            assert f.is_file(), str(f)
            if name not in installed:
                body=f.read_text(encoding='utf-8')
                assert body.startswith('---\n') and f'name: {name}\n' in body
                installed.add(name)
        for external in p['external_skills']:
            assert any(x['id']==external for x in c['external_skills']),external
    for e in c['external_skills']:
        assert re.fullmatch(r'[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+',e['repo']),e['repo']
        assert re.fullmatch(r'[a-zA-Z0-9._-]+',e['name']),e['name']
        assert e['source']==f"https://github.com/{e['repo']}"
        assert all(p in packs for p in e['packs'])
    return c


def scan_target(target):
    """Detecta stack somente por manifests, sem ler código, env ou credenciais."""
    path=Path(target).expanduser().resolve()
    if not path.is_dir():
        raise ValueError('Diretório de projeto inexistente')
    identified, evidence = scan_manifests(path)
    for group in ('apps', 'packages', 'services'):
        parent = path / group
        if not parent.is_dir() or not parent.resolve().is_relative_to(path):
            continue
        for child in sorted(parent.iterdir())[:50]:
            if not child.is_dir() or not child.resolve().is_relative_to(path):
                continue
            packs, signs = scan_manifests(child)
            identified.update(packs)
            if signs:
                evidence.append(child.relative_to(path).as_posix() + ': ' + ', '.join(signs))
    return sorted(identified), evidence


def scan_manifests(path):
    identified={'engineering'}
    evidence=[]
    pkg=path/'package.json'
    if pkg.is_file():
        try:
            data=json.loads(pkg.read_text(encoding='utf-8'))
            deps={**data.get('dependencies',{}),**data.get('devDependencies',{})}
            if any(k in deps for k in ('react','react-dom','@vitejs/plugin-react')):
                identified.update(['frontend','design','accessibility','qa-testing']);evidence.append('React em package.json')
            if 'next' in deps:
                identified.update(['nextjs','frontend','seo','performance']);evidence.append('Next.js em package.json')
            if any(k in deps for k in ('react-native','expo')):
                identified.add('mobile');evidence.append('React Native/Expo em package.json')
            if any(k in deps for k in ('@nestjs/core','express','fastify','hono')):
                identified.add('backend-node');evidence.append('Backend Node em package.json')
            if any(k in deps for k in ('@prisma/client','prisma','drizzle-orm','pg','@supabase/supabase-js')):
                identified.add('database');evidence.append('Cliente SQL/Postgres em package.json')
            if any(k in deps for k in ('stripe','@stripe/stripe-js')):
                identified.add('payments');evidence.append('Stripe em package.json')
            if any(k in deps for k in ('@sentry/node','@sentry/nextjs','@sentry/react')):
                identified.add('observability');evidence.append('Sentry em package.json')
            if any(k in deps for k in ('ai','@ai-sdk/openai','langchain')):
                identified.add('ai-apps');evidence.append('IA em package.json')
        except (OSError,ValueError,TypeError):
            evidence.append('package.json inválido: detecção parcial')
    pyproject=path/'pyproject.toml'
    requirements=path/'requirements.txt'
    if pyproject.is_file() or requirements.is_file():
        # Limite de leitura; arquivos de requirements podem conter URLs privadas.
        identified.add('backend-python');evidence.append('Manifest Python presente')
    composer=path/'composer.json'
    if composer.is_file():
        identified.add('backend-php');evidence.append('Composer presente')
    for label, manifests in (
        ('JVM', ('pom.xml', 'build.gradle', 'build.gradle.kts', 'settings.gradle', 'settings.gradle.kts')),
        ('Go', ('go.mod',)),
        ('Rust', ('Cargo.toml',)),
        ('Ruby', ('Gemfile',)),
    ):
        if any((path / name).is_file() for name in manifests):
            identified.add('qa-testing')
            evidence.append(label + ' por manifesto; usar verificações da stack real')
    if any(next(path.glob(pattern), None) for pattern in ('*.sln', '*.slnx', '*.csproj', '*.fsproj')):
        identified.add('qa-testing')
        evidence.append('.NET por manifesto; usar verificações da stack real')
    if (path / 'pubspec.yaml').is_file() or any(path.glob('*.xcodeproj')):
        identified.update(('mobile', 'qa-testing'))
        evidence.append('Manifesto Flutter ou Xcode; confirmar plataformas')
    if (path/'docker-compose.yml').is_file() or (path/'compose.yaml').is_file() or (path/'.github'/'workflows').exists():
        identified.add('devops');evidence.append('Compose/CI presente')
    if (path/'wrangler.toml').is_file() or (path/'wrangler.jsonc').is_file():
        identified.add('cloudflare');evidence.append('Wrangler presente')
    if (path/'index.html').is_file() and not pkg.is_file():
        identified.update(['design','accessibility','seo']);evidence.append('Site HTML estático')
    return identified,evidence


def choice(args,c):
    ids={p['id'] for p in c['packs']}
    requested=set(args.packs or [])
    if getattr(args,'auto',False):
        guess,_=scan_target(args.target or '.')
        requested.update(guess)
    if not requested:
        raise ValueError('Selecione --packs NOME [NOME...] ou use --auto')
    invalid=requested-ids
    if invalid:raise ValueError('Packs desconhecidos: '+', '.join(sorted(invalid)))
    return sorted(requested)


def selected(packs,c):
    pp={p['id']:p for p in c['packs']}
    local=sorted({s for p in packs for s in pp[p]['local_skills']})
    remotes=sorted({e for p in packs for e in pp[p]['external_skills']})
    ext={e['id']:e for e in c['external_skills']}
    return local,[ext[k] for k in remotes]


def make_state_path(base):
    return base/STATE


def read_state(path):
    if not path.exists():return {'schema':1,'managed':{}}
    obj=json.loads(path.read_text(encoding='utf-8'))
    if obj.get('schema')!=1 or not isinstance(obj.get('managed'),dict):
        raise ValueError('Manifesto de instalação incompatível')
    return obj


def atomic(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(dir=path.parent,prefix='.'+path.name+'.')
    try:
        with os.fdopen(fd,'wb') as f:f.write(data)
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)


def list_packs(c):
    for p in c['packs']:
        print(f"{p['id']:19} local={len(p['local_skills']):2} terceiros={len(p['external_skills']):2}  {p['description']}")


def show_plan(args,c,packs):
    locals_,externals=selected(packs,c)
    base,target=paths(args)
    print('ESCOPO:',args.scope,'| destino skills:',target)
    print('PACKS:',', '.join(packs))
    print(f'SKILLS PRÓPRIAS: {len(locals_)} | TERCEIROS CATALOGADOS: {len(externals)}')
    for name in locals_:print('  [local] '+name)
    if externals:
        print('  -- downloads opcionais (sujeitos a revisão de origem e disponibilidade) --')
        for e in externals:print('  [externo] '+e['repo']+' --skill '+e['name'])
    if not args.with_external:print('SKILLS EXTERNAS: NÃO serão baixadas (adicione --with-external).')
    if not getattr(args,'apply',False):print('PRÉVIA APENAS: nenhuma modificação realizada. Use install --apply.')
    return locals_,externals


def install_local(args,locals_):
    base,target=paths(args)
    state=make_state_path(base)
    require_safe(base,base); require_safe(target,target); require_safe(state,base)
    state_obj=read_state(state)
    managed=dict(state_obj['managed'])
    changes=[];skipped=[]
    for name in locals_:
        src=ROOT/'specialties'/'skills'/name/'SKILL.md'
        dest=target/name/'SKILL.md'
        require_safe(dest,target)
        data=src.read_bytes()
        previous=dest.read_bytes() if dest.is_file() else None
        record=managed.get(str(dest))
        if previous==data: continue
        if previous is not None and (not record or digest(previous)!=record['sha256']):
            skipped.append(name);continue
        changes.append((dest,previous,data,name))
    if skipped:print('PRESERVADOS (pré-existentes ou editados):',', '.join(skipped))
    for dest,_,_,name in changes: print(('CRIAR' if not dest.exists() else 'ATUALIZAR')+' skill local: '+name)
    if not args.apply:return 0
    # Verifica todos os destinos antes de escrever qualquer arquivo.
    for dest,_,_,_ in changes:require_safe(dest,target)
    journal=[]
    try:
        for dest,prev,data,_ in changes:
            atomic(dest,data);journal.append((dest,prev))
            managed[str(dest)]={'sha256':digest(data),'origin':'created' if prev is None else 'managed'}
        old_state=state.read_bytes() if state.is_file() else None
        atomic(state,(json.dumps({'schema':1,'managed':managed},ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    except Exception:
        for dest,prev in reversed(journal):
            if prev is None: dest.unlink(missing_ok=True)
            else:atomic(dest,prev)
        if 'old_state' in locals():
            if old_state is None:state.unlink(missing_ok=True)
            else:atomic(state,old_state)
        raise
    print('SKILLS PRÓPRIAS INSTALADAS/ATUALIZADAS:',len(changes))
    return 1 if skipped else 0


def install_external(args,entries):
    if not args.apply or not args.with_external or not entries:return 0
    if len(entries)>args.max_external and not args.allow_large:
        print(f'ABORTADO: {len(entries)} skills externas. Limite={args.max_external}; escolha menos packs ou --allow-large.')
        return 2
    if not shutil.which('git'):
        print('Falta Git para instalar skills externas.');return 2
    node='npx.cmd' if os.name=='nt' else 'npx'
    if not shutil.which(node):print('Falta npx; instale Node 22.20+.');return 2
    version=json.loads((ROOT/'catalog'/'versions.json').read_text(encoding='utf-8'))['npm']['skills']
    cmdbase=[node,'-y','skills@'+version,'add']
    failures=[]
    for e in entries:
        argv=cmdbase+[e['repo'],'--skill',e['name'],'-a','codex','-y','--copy']
        if args.scope=='global':argv+=['-g']
        target_cwd=(args.target or str(ROOT)) if args.scope=='project' else str(ROOT)
        print('INSTALANDO (terceiro): '+e['repo']+' / '+e['name'])
        try:
            res=subprocess.run(argv,cwd=target_cwd,text=True,capture_output=True,errors='replace',timeout=420)
            if res.returncode:
                failures.append(e['id']);print('  ERRO (saída suprimida para evitar segredos)')
            else:print('  OK')
        except (OSError,subprocess.TimeoutExpired):
            failures.append(e['id']);print('  ERRO / TIMEOUT')
    if failures:print('PENDENTES (fonte/nome/compatibilidade):',', '.join(failures))
    print('Skills de terceiros são gerenciadas pela CLI skills; audite/atualize via npx skills list/check/update.')
    return 1 if failures else 0


def audit(args):
    base,target=paths(args)
    state=read_state(make_state_path(base))
    errors=[]
    for raw,entry in sorted(state['managed'].items()):
        file=Path(raw)
        try:
            require_safe(file,target)
            status='OK' if file.is_file() and digest(file.read_bytes())==entry['sha256'] else 'ALTERADO/AUSENTE'
        except ValueError:status='DESTINO INVALIDO'
        print(status, file.name, file.parent.name)
        if status!='OK':errors.append(raw)
    print('Auditoria de arquivos locais:',len(state['managed']),'registrados;',len(errors),'divergências')
    print('Não verifica skills de terceiros ou se o Codex as carregou em tempo de execução.')
    return 1 if errors else 0


def uninstall(args):
    base,target=paths(args)
    state_path=make_state_path(base)
    state=read_state(state_path)
    kept={};removed=0
    for raw,entry in sorted(state['managed'].items()):
        path=Path(raw);require_safe(path,target)
        if not path.is_file() or digest(path.read_bytes())!=entry['sha256'] or entry['origin']!='created':
            kept[raw]=entry;print('PRESERVADO:',path.name);continue
        print('REMOVER:',path.parent.name)
        if args.apply:
            path.unlink();removed+=1
            try:path.parent.rmdir()
            except OSError:pass
        else:kept[raw]=entry
    if args.apply:
        if kept:atomic(state_path,(json.dumps({'schema':1,'managed':kept},indent=2)+'\n').encode('utf-8'))
        else:state_path.unlink(missing_ok=True)
    print('Removidos:',removed,'| Nenhuma skill externa desinstalada; remova pelo gerenciador original.')
    return 0


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='cmd',required=True)
    sub.add_parser('list');sub.add_parser('validate')
    for action in ('recommend','plan','install','audit','uninstall'):
        p=sub.add_parser(action)
        p.add_argument('--scope',choices=['project','global'],default='project')
        p.add_argument('--target',default='.',help='Diretório do projeto (escopo project)')
        if action in ('plan','install'):
            p.add_argument('--packs',nargs='+',default=[])
            p.add_argument('--auto',action='store_true',help='Detectar a stack por manifests')
            p.add_argument('--with-external',action='store_true',help='Instalar skills remotas (requer --apply)')
            p.add_argument('--max-external',type=int,default=16)
            p.add_argument('--allow-large',action='store_true')
        if action in ('install','uninstall'):
            p.add_argument('--apply',action='store_true',help='Permitir gravação de arquivos')
    args=parser.parse_args(argv)
    try:
        c=validate_catalog()
        if args.cmd=='validate':print('Catálogo OK:',len(c['packs']),'packs;',len(c['external_skills']),'skills externas');return 0
        if args.cmd=='list':list_packs(c);return 0
        if args.cmd=='recommend':
            names,evidence=scan_target(args.target)
            print('Packs recomendados:',', '.join(names))
            print('Evidências:',', '.join(evidence) or 'nenhuma stack detectada; apenas engenharia')
            print('Detecção heurística; revise os packs antes de instalar.');return 0
        if args.cmd=='audit':return audit(args)
        if args.cmd=='uninstall':return uninstall(args)
        packs=choice(args,c)
        locals_,externals=show_plan(args,c,packs)
        if args.cmd=='plan':return 0
        if args.apply and args.with_external and len(externals)>args.max_external and not args.allow_large:
            print('ABORTADO: limite de downloads; use menos packs ou --allow-large (se revisado).');return 2
        if args.apply and args.with_external and externals:
            import shutil
            if not shutil.which('git') or not shutil.which('npx.cmd' if os.name=='nt' else 'npx'):
                print('ABORTADO: Git e npx são necessários para downloads. Nenhum arquivo local alterado.')
                return 2
        result=install_local(args,locals_)
        return max(result, install_external(args,externals))
    except (OSError,ValueError,AssertionError,KeyError,json.JSONDecodeError) as e:
        print('ERRO:',str(e)[:250],file=sys.stderr);return 1

if __name__=='__main__':sys.exit(main())
