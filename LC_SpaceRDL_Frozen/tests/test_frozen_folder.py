"""Packaging/regeneration regression; no software-runtime completion claim."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('regenerator', ROOT / 'scripts/regenerate_docs.py')
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)


class FrozenFolderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='.regeneration_test_', dir=ROOT)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'data').mkdir()
        for name in ('requirements.json', 'resources.json', 'data_fragment_statements.json', 'strict_audit.json', 'code.rdl', 'data/issues.json'):
            shutil.copyfile(ROOT / name, self.root / name)

    def input_hashes(self):
        return {str(path.relative_to(self.root)): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in sorted(self.root.rglob('*.json'))}

    def outputs(self):
        return {path.name: path.read_bytes() for path in sorted(self.root.glob('*.md'))}

    def test_regeneration_keeps_manual_issue_status_and_reviews(self):
        path = self.root / 'data/issues.json'
        issues = json.loads(path.read_text())
        issues['issues'][0]['status'] = 'manual-reviewed-regression-sentinel'
        issues['issues'][0]['review'] = '人工修改保留哨兵'
        path.write_text(json.dumps(issues, ensure_ascii=False))
        path = self.root / 'requirements.json'
        req = json.loads(path.read_text())
        req['requirements'][0]['review'] = '需求人工审查保留哨兵'
        path.write_text(json.dumps(req, ensure_ascii=False))
        before = self.input_hashes()
        generator.render(self.root)
        self.assertEqual(before, self.input_hashes())
        self.assertIn('人工修改保留哨兵', (self.root / 'issues.md').read_text())
        self.assertIn('manual-reviewed-regression-sentinel', (self.root / 'issues.md').read_text())
        self.assertIn('需求人工审查保留哨兵', (self.root / 'requirements.md').read_text())

    def test_regeneration_is_deterministic(self):
        generator.render(self.root)
        first = self.outputs()
        generator.render(self.root)
        self.assertEqual(first, self.outputs())

    def test_new_documents_use_current_projection_positions(self):
        generator.render(self.root)
        atoms = json.loads((self.root / 'data_fragment_statements.json').read_text())
        md = (self.root / 'statements.md').read_text()
        for atom in atoms:
            for line in atom['projection_lines']:
                self.assertIn(f'[code.rdl L{line}]', md)
        self.assertEqual(len(atoms), 282)


if __name__ == '__main__':
    unittest.main()
