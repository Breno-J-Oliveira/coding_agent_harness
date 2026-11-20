"""Tests for routing, token reporting, safety and manual kit upgrades."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'scripts'
sys.path.insert(0,str(SCRIPTS))
import devkit
from importlib.machinery import SourceFileLoader


def load(name,filename):
    spec=importlib.util.spec_from_file_location(name,SCRIPTS/filename)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tokens=load('tokens','token-report.py')
router=load('router','route-task.py')


class TokenTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name)

    def log(self,events):
        name=self.base/f'{len(list(self.base.iterdir()))}.jsonl'
        name.write_text('\n'.join(json.dumps(e) for e in events)+'\n')
        return name

    def test_reads_real_usage_only(self):
        file=self.log([{'type':'item.completed','item':{'text':'SECRET_TOKEN'}} ,
                       {'type':'turn.completed','usage':{'input_tokens':100,'cached_input_tokens':80,'output_tokens':10}}])
        data=tokens.summarize(file)
        self.assertEqual(data['total_tokens'],110)
        self.assertEqual(data['non_cached_input_tokens'],20)

    def test_refuses_missing_usage(self):
        file=self.log([{'type':'turn.started'}])
        with self.assertRaises(ValueError):tokens.summarize(file)

    def test_computes_savings_and_negative_regressions(self):
        a={'total_tokens':100,'input_tokens':80}
        b={'total_tokens':20,'input_tokens':15}
        c={'total_tokens':130,'input_tokens':110}
        self.assertEqual(tokens.compare(a,b)['total_reduction_pct'],80.0)
        self.assertEqual(tokens.compare(a,c)['total_reduction_pct'],-30.0)

    def test_rejects_negative_token_counts(self):
        file=self.log([{'type':'turn.completed','usage':{'input_tokens':-10}}])
        with self.assertRaises(ValueError):tokens.summarize(file)

    def test_multiple_turns_and_failures(self):
        file=self.log([{'type':'turn.completed','usage':{'input_tokens':50,'output_tokens':5}},
                       {'type':'turn.failed'},{'type':'turn.completed','usage':{'input_tokens':70,'output_tokens':20}}])
        data=tokens.summarize(file)
        self.assertEqual(data['turns'],2)
        self.assertEqual(data['failures'],1)
        self.assertEqual(data['total_tokens'],145)

    def test_fixture_comparison(self):
        file=ROOT/'benchmarks/fixtures/baseline.jsonl'
        other=ROOT/'benchmarks/fixtures/optimized.jsonl'
        result=tokens.compare(tokens.summarize(file),tokens.summarize(other))
        self.assertAlmostEqual(result['total_reduction_pct'],64.29,places=1)


class RoutingTests(unittest.TestCase):
    def test_trivial_file_read_no_agents(self):
        self.assertEqual(router.route('ler arquivo')['agents'],[])

    def test_security_is_sensitive(self):
        data=router.route('Auditar vulnerabilidade e auth na API de pagamento',risk='high')
        self.assertEqual(data['risk'],'elevado')
        self.assertIn('security',data['agents'])

    def test_frontend_visual_uses_least_three(self):
        data=router.route('Auditar layout, css, frontend e react, verificar SEO e design mobile.')
        self.assertLessEqual(len(data['agents']),3)

    def test_no_invented_model(self):
        self.assertNotIn('gpt-',json.dumps(router.route('buscar função'),ensure_ascii=False))


class InstallSafetyTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.home=Path(self.tmp.name)/'home';self.home.mkdir()
        self.env={**os.environ,'HOME':str(self.home),'USERPROFILE':str(self.home),'CODEX_HOME':str(self.home/'.codex')}

    def call(self,*argv,env=None,rc=0):
        result=subprocess.run([sys.executable,str(SCRIPTS/'devkit.py'),*argv],env=env or self.env,
                              text=True,capture_output=True,cwd=ROOT,timeout=30)
        self.assertEqual(result.returncode,rc,result.stdout+result.stderr)
        return result.stdout

    def test_skills_apply_requires_node_git(self):
        env={**self.env,'PATH':''}
        out=self.call('install','--apply','--with-skills',env=env,rc=1)
        self.assertFalse((self.home/'.codex').exists())

    def test_applying_without_external_flags_does_not_require_node(self):
        env={**self.env,'PATH':''}
        self.call('install','--apply',env=env)
        self.assertTrue((self.home/'.codex/config.toml').exists())

    def test_state_drift_is_not_overwritten(self):
        self.call('install','--apply')
        cfg=self.home/'.codex/config.toml'
        cfg.write_text(cfg.read_text()+'\n# user-customization\n')
        out=self.call('install','--apply',rc=1)
        self.assertIn('PRESERVADO',out)
        self.assertIn('user-customization',cfg.read_text())

    def test_model_profile_generator_offline(self):
        output=Path(self.tmp.name)/'profiles'
        script=SCRIPTS/'build-model-profile.py'
        res=subprocess.run([sys.executable,str(script),'--cheap-model','vendor-lite',
                            '--strong-model','vendor-pro','--output',str(output)],
                           text=True,capture_output=True,timeout=30)
        self.assertEqual(res.returncode,0,res.stdout+res.stderr)
        self.assertEqual(len(list(output.glob('*.toml'))),28)
        self.assertTrue((output.parent/'role-routing-manifest.json').is_file())

    def test_upgrade_owned_file(self):
        base=self.home/'.codex';agent=base/'agents';skills=self.home/'.agents/skills';rules=base/'AGENTS.md'
        manager=devkit.ManagedFiles(base,agent,skills,rules,True)
        manager.put(agent/'backend.toml',b'name = "backend"\n','agent')
        manager.save()
        updated=devkit.ManagedFiles(base,agent,skills,rules,True)
        updated.put(agent/'backend.toml',b'name = "backend"\ndescription = "new"\n','agent')
        updated.save()
        self.assertIn(b'description', (agent/'backend.toml').read_bytes())

    def test_manual_edit_blocks_auto_upgrade(self):
        base=self.home/'.codex';agent=base/'agents';skills=self.home/'.agents/skills';rules=base/'AGENTS.md'
        mgr=devkit.ManagedFiles(base,agent,skills,rules,True)
        path=agent/'backend.toml'
        mgr.put(path,b'original','agent');mgr.save()
        path.write_bytes(b'user customized')
        next_version=devkit.ManagedFiles(base,agent,skills,rules,True)
        next_version.put(path,b'upgraded','agent')
        self.assertEqual(path.read_bytes(),b'user customized')
        self.assertEqual(len(next_version.skips),1)

    def test_transaction_rollback(self):
        base=self.home/'.codex';agent=base/'agents';skills=self.home/'.agents/skills';rules=base/'AGENTS.md'
        mgr=devkit.ManagedFiles(base,agent,skills,rules,True)
        mgr.put(agent/'backend.toml',b'temporary','agent')
        mgr.undo_on_error()
        self.assertFalse((agent/'backend.toml').exists())


if __name__=='__main__':unittest.main()
