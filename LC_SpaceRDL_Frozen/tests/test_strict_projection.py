"""Regress partial projection checks. These are not LC or official parser tests."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('partial_shape_checker',ROOT/'scripts/check_data_projection.py')
checker=importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class StrictProjectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='strict_check_',dir=ROOT)
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        for name in ('resources.json','data_fragments.rdl','data_fragment_statements.json','strict_audit.json'):
            shutil.copyfile(ROOT/name,self.root/name)

    def replace_code(self, old, new):
        path=self.root/'data_fragments.rdl'
        text=path.read_text()
        self.assertIn(old,text)
        path.write_text(text.replace(old,new,1))

    def check_fails(self):
        report=checker.check(self.root)
        self.assertEqual(report['result'],'fail')
        self.assertTrue(report['errors'])
        self.assertFalse(json.loads((self.root/'strict_audit.json').read_text())['strict_full_conversion_complete'])

    def test_actual_data_projection_passes_but_full_remains_blocked(self):
        report=checker.check(self.root)
        self.assertEqual(report['result'],'pass')
        self.assertEqual(report['distinct_data_atoms'],282)
        audit=json.loads((self.root/'strict_audit.json').read_text())
        self.assertEqual(audit['result'],'blocked-full-conversion')
        self.assertFalse(audit['strict_full_conversion_complete'])

    def test_rejects_software_native_call_in_data_projection(self):
        path=self.root/'data_fragments.rdl'
        path.write_text(path.read_text()+'SendData LCEventService LCEventData0106;\n')
        self.check_fails()

    def test_rejects_extra_compute_function_name(self):
        self.replace_code('Compute ','Compute InventedFunction ')
        self.check_fails()

    def test_rejects_short_reference_keyword(self):
        self.replace_code('ReqCapByFormTable','ReqCapByTable')
        self.check_fails()

    def test_rejects_unregistered_formula(self):
        self.replace_code('FormulaTable.','FormulaTable.Missing')
        self.check_fails()

    def test_rejects_field_access_as_atom_operand(self):
        self.replace_code('Compute ','Compute Context.field ')
        self.check_fails()

    def test_rejects_unbalanced_structure(self):
        self.replace_code('Composite {','Composite ')
        self.check_fails()

    def test_rejects_unknown_guard(self):
        path=self.root/'data_fragments.rdl'
        path.write_text(path.read_text()+'If (UnknownGuard) {\n}\n')
        self.check_fails()

    def test_rejects_else_without_if(self):
        path=self.root/'data_fragments.rdl'
        path.write_text(path.read_text()+'} Else {\n}\n')
        self.check_fails()

    def test_rejects_wrong_catalog_excerpt(self):
        path=self.root/'data_fragment_statements.json'
        doc=json.loads(path.read_text())
        doc[0]['source_excerpt']='Set UnreviewedTarget UnreviewedValue;'
        path.write_text(json.dumps(doc))
        self.check_fails()

    def test_all_44_unconfirmed_calls_are_rejected_not_promoted(self):
        audit=json.loads((self.root/'strict_audit.json').read_text())
        self.assertEqual(len(audit['rejected_statements']),44)
        self.assertEqual(audit['rejected_operator_counts'],{'SendData':27,'GetData':7,'ProTC':6,'ProTM':1,'Init':3})
        for record in audit['rejected_statements']:
            self.assertTrue(record['requirements'])
            self.assertTrue(record['evidence'])
            self.assertTrue(record['reason'])


if __name__=='__main__':
    unittest.main()
