import inspect
import os
import unittest
from nose.plugins import PluginTester
from nose_run_line_number.plugin import RunLineNumber


class SomeUnitTest(unittest.TestCase):

    def linenumtest_some_test_1(self):
        pass


    def linenumtest_some_test_2(self):
        pass


class AnotherUnitTest(unittest.TestCase):

    def linenumtest_some_test_1(self):
        pass

class TestNoseLinePlugin(PluginTester, unittest.TestCase):
    activate = '--line-file'
    plugins = [RunLineNumber()]
    suitepath = os.path.realpath(__file__).rstrip('c') # .pyc -> .py

    def setUp(self):
        pass

    def _run_test_on_line(self, line):
        self.args = ['',  '--line', str(line), '--match', 'linenumtest.*']
        super(TestNoseLinePlugin, self).setUp()

    def test_run_line_of_method_definition(self):
        lines, lineno = inspect.getsourcelines(SomeUnitTest.linenumtest_some_test_1)
        self._run_test_on_line(lineno)
        self.assertIn("Ran 1 test", self.output)
        self.assertIn("OK", self.output)

    def test_run_line_inside_method_definition(self):
        lines, lineno = inspect.getsourcelines(SomeUnitTest.linenumtest_some_test_1)
        self._run_test_on_line(lineno + 1)
        self.assertIn("Ran 1 test", self.output)
        self.assertIn("OK", self.output)

    def test_run_line_past_method_definition(self):
        lines, lineno = inspect.getsourcelines(SomeUnitTest.linenumtest_some_test_1)
        self._run_test_on_line(lineno + len(lines))
        self.assertIn("Ran 1 test", self.output)
        self.assertIn("OK", self.output)

    def test_run_line_before_any_method_definitions_skips_test(self):
        self._run_test_on_line(1)
        self.assertIn("Ran 0 tests", self.output)
        self.assertIn("OK", self.output)


class TestNoseLinePluginClassRunner(PluginTester, unittest.TestCase):
    activate = '--line-file'
    plugins = [RunLineNumber()]
    suitepath = os.path.realpath(__file__).rstrip('c') # .pyc -> .py

    def setUp(self):
        pass

    def _run_test_on_line(self, line):
        self.args = ['',  '--line', str(line), '--match', 'linenumtest.*', '--level', 'class']
        super(TestNoseLinePluginClassRunner, self).setUp()

    def test_run_line_of_class_definition_runs_all_tests(self):
        lines, lineno = inspect.getsourcelines(SomeUnitTest)
        self._run_test_on_line(lineno)
        self.assertIn("Ran 2 tests", self.output)
        self.assertIn("OK", self.output)

    def test_run_line_of_method_definition_runs_all_tests(self):
        lines, lineno = inspect.getsourcelines(SomeUnitTest.linenumtest_some_test_1)
        self._run_test_on_line(lineno)
        self.assertIn("Ran 2 tests", self.output)
        self.assertIn("OK", self.output)

    def test_run_line_inside_method_definition_runs_all_tests(self):
        lines, lineno = inspect.getsourcelines(SomeUnitTest.linenumtest_some_test_2)
        self._run_test_on_line(lineno + 1)
        self.assertIn("Ran 2 tests", self.output)
        self.assertIn("OK", self.output)

    def test_run_line_past_method_definitions_runs_all_tests(self):
        lines, lineno = inspect.getsourcelines(SomeUnitTest.linenumtest_some_test_1)
        self._run_test_on_line(lineno + len(lines))
        self.assertIn("Ran 2 tests", self.output)
        self.assertIn("OK", self.output)

    def test_run_line_before_any_class_definitions_skips_tests(self):
        self._run_test_on_line(1)
        self.assertIn("Ran 0 tests", self.output)
        self.assertIn("OK", self.output)
