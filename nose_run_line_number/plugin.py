__test__ = False

import logging
import os
import ast
from nose.plugins import Plugin
from nose.util import src, set

log = logging.getLogger('nose.plugins.runlinenumber')

class MethodFinder(ast.NodeVisitor):
    def __init__(self, line_to_match, test_pattern):
        self.matched_function = None
        self.line_to_match = line_to_match
        self.test_pattern = test_pattern

    def visit_FunctionDef(self, node):
        if self.test_pattern.match(node.name):
            self.current_function = node.name

        self.generic_visit(node)

    def generic_visit(self, node):
        if self.line_to_match == getattr(node, 'lineno', -1):
            self.matched_function = self.current_function

        super(MethodFinder, self).generic_visit(node)

class RunLineNumber(Plugin):
    name = 'runlinenumber'

    def options(self, parser, env=os.environ):
        parser.add_option('--line', dest='linenum', metavar='LINE', type='int', help="Run test specified on this line")
        parser.add_option('--line-file', dest='linefile', metavar='File', help="file to run the test on (used for setuptools integration)")

    def configure(self, options, conf):
        if options.linenum:
            self.enabled = True

            if options.linefile:
                test_name = options.linefile
            else:
                if len(conf.testNames) < 1:
                    log.error("must specify a test file to run")
                    self.matched_function = None
                    return

                test_name = self.findTestName(conf.testNames)

            with open(test_name, 'r') as f:
                ast_node = ast.parse(f.read())
            finder = MethodFinder(options.linenum, conf.testMatch)
            finder.visit(ast_node)
            self.matched_function = finder.matched_function
            log.info("Matched function: %s with line %d" % (self.matched_function, options.linenum))

    def findTestName(self, testNames):
        if testNames[0] == '.' and len(testNames) > 1:
            return testNames[1]
        else:
            return testNames[0]

    def wantMethod(self, method):
        return method.im_func.func_name == self.matched_function
