import os
from collections import defaultdict
from unittest.case import SkipTest

from nose.plugins.errorclass import ErrorClassPlugin
from nose.failure import Failure


class SummaryReporter(ErrorClassPlugin):
    name = 'summary-report'

    # override
    def options(self, parser, env):
        ErrorClassPlugin.options(self, parser, env)
        parser.add_option(
            '--summary-report-on', choices=('top-module', 'module-path', 'class'),
            default='top-module',
            help='How to aggregate the results in the report based on the module/class paths of the test functions')

    # override
    def configure(self, options, conf):
        ErrorClassPlugin.configure(self, options, conf)
        self.summary_report_on = options.summary_report_on
        self.columns = ['success', 'error', 'failure', 'skip']
        self.stats = defaultdict(lambda: {status: 0 for status in self.columns})
        self.skipped_tests_msgs = set()

    # override
    def addSuccess(self, test):
        row_key = self._row_key_from_test(test)
        self.stats[row_key]['success'] += 1

    # override
    def addError(self, test, err, capt=None):
        row_key = self._row_key_from_test(test)
        err_cls, exception, _ = err
        if err_cls is SkipTest:
            self.stats[row_key]['skip'] += 1
            self.skipped_tests_msgs.add(str(exception))
        else:
            self.stats[row_key]['error'] += 1

    # override
    def addFailure(self, test, err, capt=None):
        row_key = self._row_key_from_test(test)
        self.stats[row_key]['failure'] += 1

    # override
    def report(self, stream):
        # Note: invoking pdb in this method or in add* methods does not work, define a finalize(self, result) method instead
        non_empty_columns = [status for status in self.columns if any(self.stats[key][status] for key in self.stats)]
        if not non_empty_columns:
            return
        max_col_len = max(len(status) for status in non_empty_columns)
        max_key_len = max(len(key or '') for key in self.stats.keys())
        header_format = '{:>' + str(max_key_len) + '}' + (' | {:' + str(max_col_len) + '}') * len(non_empty_columns)
        row_format = '{row_key:>' + str(max_key_len) + '} | ' + ' | '.join('{' + status + ':' + str(max_col_len) + '}' for status in non_empty_columns)
        stream.writeln('-' * 70)
        stream.writeln('Summary:')
        stream.writeln(header_format.format(self.summary_report_on, *non_empty_columns))
        stream.writeln('   ' + '-' * (max_key_len + len(non_empty_columns) * (max_col_len + 3)))
        for row_key in sorted(self.stats.keys()):
            if row_key:  # can be an empty string
                stats = self.stats[row_key]
                stats['row_key'] = row_key
                stream.writeln(row_format.format(**stats))
        if self.skipped_tests_msgs:
            stream.writeln('\nThere were some skipped tests messages:')
            for msg in self.skipped_tests_msgs:
                stream.writeln('- ' + msg)

    def _row_key_from_test(self, test):
        class_name = ''
        if hasattr(test, 'address'):
            _, module_path, method = test.address()
            if method and '.' in method:
                class_name, method = method.split('.')
        elif hasattr(test, 'context'):
            module_path = test.context.__module__
            class_name = test.context.__name__
        else:
            module_path, class_name, method = test.id().rsplit('.', 2)
            if class_name[0].islower():
                module_path += '.' + class_name
                class_name = ''
        return {
            'module-path': module_path,
            'top-module': module_path.split('.', 1)[0],
            'class': class_name
        }[self.summary_report_on]
