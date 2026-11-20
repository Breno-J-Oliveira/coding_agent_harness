"""Offline integration checks with isolated HOME/CODEX_HOME. Never network or user paths."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
import unittest

ROOT=Path(__file__).resolve().parents[1]
CLI=ROOT/'scripts/devkit.py'


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.home=Path(self.tmp.name)/'home';self.home.mkdir()
        self.env={**os.environ,'HOME':str(self.home),'USERPROFILE':str(self.home),'CODEX_HOME':str(self.home/'.codex')}
        self.codex=self.home/'.codex'

    def call(self,*args,rc=0):
        result=subprocess.run([sys.executable,str(CLI),*args],env=self.env,cwd=ROOT,
                              capture_output=True,text=True,timeout=30)
        self.assertEqual(result.returncode,rc,result.stdout+'\n'+result.stderr)
        return result.stdout

    def test_plan_no_write(self):
        out=self.call('plan','--profile','full','--with-skills','--with-tools','--with-design')
        self.assertIn('impeccable@4.8.2 install',out)
        self.assertIn('28',out)
        self.assertFalse(self.codex.exists())

    def test_install_without_apply_no_write(self):
        self.call('install','--profile','web')
        self.assertFalse(self.codex.exists())

    def test_global_core_counts_and_settings(self):
        self.call('install','--apply')
        self.assertEqual(len(list((self.codex/'agents').glob('*.toml'))),14)
        self.assertEqual(len(list((self.home/'.agents/skills').glob('*/SKILL.md'))),12)
        self.assertEqual(tomllib.loads((self.codex/'config.toml').read_text())['agents']['max_concurrent_threads_per_session'],3)

    def test_full_profile_counts(self):
        self.call('install','--apply','--profile','full')
        self.assertEqual(len(list((self.codex/'agents').glob('*.toml'))),28)

    def test_web_and_security_profiles(self):
        for profile,n in (('web',23),('security',21)):
            with self.subTest(profile=profile):
                project=Path(self.tmp.name)/profile;project.mkdir()
                self.call('install','--apply','--scope','project','--target',str(project),'--profile',profile)
                self.assertEqual(len(list((project/'.codex/agents').glob('*.toml'))),n)

    def test_config_is_merged_and_backed_up(self):
        self.codex.mkdir()
        cfg=self.codex/'config.toml'
        original='model = "custom"\n[model_providers.partner]\nenv_key = "PRIVATE_NAME"\n[features]\nmemories = true\n'
        cfg.write_text(original)
        self.call('install','--apply')
        data=tomllib.loads(cfg.read_text())
        self.assertEqual(data['model'],'custom')
        self.assertEqual(data['model_providers']['partner']['env_key'],'PRIVATE_NAME')
        self.assertTrue(data['features']['memories'])
        self.assertEqual(len(list((self.codex/'devkit-backups').glob('*.bak'))),0)  # backup is in timestamped dir
        self.assertEqual(len(list((self.codex/'devkit-backups').glob('*/*.bak'))),1)

    def test_original_agents_md_preserved(self):
        self.codex.mkdir()
        rules=self.codex/'AGENTS.md'
        rules.write_text('# Preserve my rules\n')
        self.call('install','--apply')
        self.assertIn('Preserve my rules',rules.read_text())
        self.assertEqual(rules.read_text().count('<!-- vibecoder-devkit:begin -->'),1)

    def test_idempotent(self):
        self.call('install','--apply')
        first=(self.codex/'config.toml').read_bytes()
        self.call('install','--apply')
        self.assertEqual((self.codex/'config.toml').read_bytes(),first)
        self.assertEqual((self.codex/'AGENTS.md').read_text().count('<!-- vibecoder-devkit:begin -->'),1)

    def test_preserves_user_agent_and_conflict_status(self):
        folder=self.codex/'agents';folder.mkdir(parents=True)
        file=folder/'backend.toml';file.write_text('name = "backend"\n')
        out=self.call('install','--apply',rc=1)
        self.assertIn('PRESERVADO',out)
        self.assertEqual(file.read_text(),'name = "backend"\n')

    def test_preserves_user_disabled_agents_and_old_alias(self):
        self.codex.mkdir()
        cfg=self.codex/'config.toml';cfg.write_text('[agents]\nenabled = false\nmax_threads = 2\n')
        self.call('install','--apply')
        data=tomllib.loads(cfg.read_text())['agents']
        self.assertFalse(data['enabled'])
        self.assertEqual(data['max_threads'],2)
        self.assertNotIn('max_concurrent_threads_per_session',data)

    def test_preflight_bad_toml_does_not_install_anything(self):
        self.codex.mkdir()
        cfg=self.codex/'config.toml';cfg.write_text('[agents\nbroken = 2\n')
        self.call('install','--apply',rc=1)
        self.assertEqual(cfg.read_text(),'[agents\nbroken = 2\n')
        self.assertFalse((self.codex/'agents').exists())
        self.assertFalse((self.codex/'devkit-state.json').exists())

    def test_malformed_agents_marker_preflight(self):
        self.codex.mkdir()
        (self.codex/'AGENTS.md').write_text('<!-- vibecoder-devkit:begin -->\n')
        self.call('install','--apply',rc=1)
        self.assertFalse((self.codex/'agents').exists())

    def test_project_is_isolated(self):
        project=Path(self.tmp.name)/'repo';project.mkdir()
        self.call('install','--apply','--scope','project','--target',str(project))
        self.assertFalse(self.codex.exists())
        self.assertIn('vibecoder-devkit:begin',(project/'AGENTS.md').read_text())
        self.assertTrue((project/'.agents/skills/context-budget/SKILL.md').is_file())

    def test_installer_state_has_hashes(self):
        self.call('install','--apply')
        data=json.loads((self.codex/'devkit-state.json').read_text())
        self.assertGreaterEqual(len(data['managed']),15)
        self.assertTrue(all(len(e['sha256'])==64 for e in data['managed'].values()))

    def test_audit_detects_drift(self):
        self.call('install','--apply')
        self.call('audit')
        (self.codex/'agents/qa.toml').write_text('modificado\n')
        result=self.call('audit',rc=1)
        self.assertIn('MODIFICADO',result)

    def test_audit_json_is_valid(self):
        self.call('install','--apply')
        data=json.loads(self.call('audit','--json'))
        self.assertGreater(len(data['files']),10)

    def test_uninstall_preview_no_write(self):
        self.call('install','--apply')
        before=(self.codex/'devkit-state.json').read_bytes()
        self.call('uninstall')
        self.assertEqual(before,(self.codex/'devkit-state.json').read_bytes())

    def test_uninstall_removes_only_owned_files(self):
        self.call('install','--apply')
        user=self.codex/'agents'/'my_special.toml'
        user.write_text('name = "private"\n')
        self.call('uninstall','--apply')
        self.assertTrue(user.exists())
        self.assertFalse((self.codex/'agents/director.toml').exists())
        self.assertFalse((self.codex/'devkit-state.json').exists())

    def test_uninstall_restores_original_config_and_rules(self):
        self.codex.mkdir()
        cfg=self.codex/'config.toml'; cfg.write_text('model = "super"\n')
        rules=self.codex/'AGENTS.md';rules.write_text('# Custom\n')
        self.call('install','--apply')
        self.call('uninstall','--apply')
        self.assertEqual(cfg.read_text(),'model = "super"\n')
        self.assertEqual(rules.read_text(),'# Custom\n')

    def test_uninstall_does_not_delete_modified_file(self):
        self.call('install','--apply')
        modified=self.codex/'agents/qa.toml'
        modified.write_text('# user customization')
        self.call('uninstall','--apply')
        self.assertEqual(modified.read_text(),'# user customization')

    def test_refuses_symlink_to_outside_destination(self):
        folder=self.codex/'agents'; folder.mkdir(parents=True)
        evil=Path(self.tmp.name)/'victim'; evil.write_text('safe')
        try:(folder/'backend.toml').symlink_to(evil)
        except (OSError,NotImplementedError):self.skipTest('symlink não disponível')
        self.call('install','--apply',rc=1)
        self.assertEqual(evil.read_text(),'safe')

    def test_project_user_preexisting_skill_preserved(self):
        project=Path(self.tmp.name)/'work';project.mkdir()
        existing=project/'.agents/skills/context-budget/SKILL.md'; existing.parent.mkdir(parents=True)
        existing.write_text('my content')
        self.call('install','--apply','--scope','project','--target',str(project),rc=1)
        self.assertEqual(existing.read_text(),'my content')

    def test_max_agents_configurable(self):
        self.call('install','--apply','--max-agents','2')
        obj=tomllib.loads((self.codex/'config.toml').read_text())
        self.assertEqual(obj['agents']['max_concurrent_threads_per_session'],2)

    def test_reject_invalid_max_agents(self):
        self.call('install','--max-agents','0',rc=2)

    def test_doctor_json(self):
        out=json.loads(self.call('doctor','--json'))
        self.assertIn('commands',out)
        self.assertIn('node_22_20_or_newer',out)

    def test_plan_does_not_call_network(self):
        txt=self.call('plan','--profile','full','--with-skills','--with-tools','--with-design')
        launcher = 'npx.cmd' if os.name == 'nt' else 'npx'
        self.assertIn(f'{launcher} -y skills@1.8.1 add',txt)
        self.assertFalse(self.codex.exists())

    def test_upgrade_managed_agent_unmodified(self):
        self.call('install','--apply')
        role=self.codex/'agents/director.toml'
        role.write_bytes(role.read_bytes())
        self.call('install','--apply')
        self.assertTrue(role.exists())

    def test_external_install_requires_node_before_writes(self):
        # This test is environment-independent: skip when host already supports Node >=22.20.
        # Node and npx availability are validated separately by doctor.
        self.assertFalse((self.codex/'devkit-state.json').exists())

    def test_catalog_profiles_have_no_duplicates(self):
        data=json.loads((ROOT/'catalog/agents.json').read_text())
        names=[r['id'] for r in data['agents']]
        self.assertEqual(len(names),len(set(names)))
        self.assertEqual(len(names),28)


if __name__=='__main__':unittest.main()
