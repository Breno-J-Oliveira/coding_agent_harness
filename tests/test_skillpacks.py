import importlib.util
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('skillpacks',ROOT/'scripts'/'skillpacks.py')
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class SkillPacksTests(unittest.TestCase):
    def cli(self,*args):
        return subprocess.run([sys.executable,str(ROOT/'scripts'/'skillpacks.py'),*map(str,args)],capture_output=True,text=True,timeout=30)

    def test_catalog_valid_and_counts(self):
        cat=mod.validate_catalog()
        self.assertGreaterEqual(len(cat['packs']),20)
        self.assertGreaterEqual(len(cat['external_skills']),50)
        self.assertEqual(len(list((ROOT/'specialties/skills').glob('*/SKILL.md'))),49)

    def test_list_and_plan_no_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            self.assertEqual(self.cli('list').returncode,0)
            r=self.cli('plan','--packs','design','seo','--target',p)
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertIn('PRÉVIA APENAS',r.stdout)
            self.assertFalse((p/'.agents').exists())

    def test_recommend_react_next(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            (p/'package.json').write_text(json.dumps({'dependencies':{'next':'16.3.2','react':'19','@prisma/client':'7'}}))
            r=self.cli('recommend','--target',p)
            self.assertEqual(r.returncode,0)
            for item in ('nextjs','frontend','database','seo'):self.assertIn(item,r.stdout)

    def test_recommend_php_python_static(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            (p/'composer.json').write_text('{}')
            (p/'requirements.txt').write_text('fastapi==0.0.1\n')
            (p/'index.html').write_text('<!DOCTYPE html>')
            rec,_=mod.scan_target(p)
            for item in ('backend-php','backend-python','seo','design'):self.assertIn(item,rec)

    def test_install_audit_and_uninstall(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            r=self.cli('install','--target',p,'--packs','design','--apply')
            self.assertEqual(r.returncode,0,r.stdout+r.stderr)
            target=p/'.agents/skills/ai-ui-pattern-audit/SKILL.md'
            self.assertTrue(target.exists())
            self.assertEqual(self.cli('audit','--target',p).returncode,0)
            r=self.cli('uninstall','--target',p,'--apply')
            self.assertEqual(r.returncode,0,r.stdout+r.stderr)
            self.assertFalse(target.exists())

    def test_install_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            args=('install','--packs','seo','--target',p,'--apply')
            self.assertEqual(self.cli(*args).returncode,0)
            self.assertEqual(self.cli(*args).returncode,0)
            self.assertEqual(self.cli('audit','--target',p).returncode,0)

    def test_preserve_existing_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);file=p/'.agents/skills/ai-ui-pattern-audit/SKILL.md'
            file.parent.mkdir(parents=True);file.write_text('own user instructions')
            result=self.cli('install','--packs','design','--target',p,'--apply')
            self.assertEqual(result.returncode,1)
            self.assertEqual(file.read_text(),'own user instructions')

    def test_modified_managed_skill_preserved_on_update(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            self.assertEqual(self.cli('install','--packs','design','--target',p,'--apply').returncode,0)
            f=p/'.agents/skills/ai-ui-pattern-audit/SKILL.md';f.write_text('edited')
            result=self.cli('install','--packs','design','--target',p,'--apply')
            self.assertEqual(result.returncode,1)
            self.assertEqual(f.read_text(),'edited')
            self.assertEqual(self.cli('audit','--target',p).returncode,1)
            self.assertEqual(self.cli('uninstall','--target',p,'--apply').returncode,0)
            self.assertEqual(f.read_text(),'edited')

    def test_symlink_target_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);outside=p/'outside';outside.mkdir()
            dest=p/'.agents'/'skills';dest.parent.mkdir()
            try:dest.symlink_to(outside,target_is_directory=True)
            except (OSError,NotImplementedError):self.skipTest('symlinks not enabled')
            result=self.cli('install','--target',p,'--packs','design','--apply')
            self.assertNotEqual(result.returncode,0)
            self.assertFalse(list(outside.iterdir()))

    def test_no_external_without_explicit_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            result=self.cli('install','--packs','engineering','--target',tmp,'--apply')
            self.assertEqual(result.returncode,0)
            self.assertNotIn('INSTALANDO (terceiro)',result.stdout)

    def test_external_guard_before_local_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            result=self.cli('install','--packs','engineering','--target',p,'--with-external','--apply','--max-external','0')
            self.assertEqual(result.returncode,2)
            self.assertFalse((p/'.agents').exists())

    def test_auto_no_manifest_only_engineering(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=self.cli('plan','--auto','--target',tmp)
            self.assertEqual(r.returncode,0)
            self.assertIn('engineering',r.stdout)

    def test_external_urls_official_github(self):
        for e in mod.catalog()['external_skills']:
            self.assertTrue(e['source'].startswith('https://github.com/'))

if __name__=='__main__':unittest.main()
