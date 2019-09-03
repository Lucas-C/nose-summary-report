import os
from collections import defaultdict

from nose.plugins import Plugin


class SummaryReporter(Plugin):
    name = 'summary-report'

    # override
    def options(self, parser, env):
        Plugin.options(self, parser, env)
        parser.add_option(
            '--summary-report-on', choices=('top-module', 'module-path', 'class'),
            default='top-module',
            help='How to aggregate the results in the report based on the module/class paths of the test functions')

    # override
    def configure(self, options, conf):
        Plugin.configure(self, options, conf)
        self.summary_report_on = options.summary_report_on
        self.columns = ['success', 'error', 'failure', 'deprecated', 'skip']
        self.stats = defaultdict(lambda: {status: 0 for status in self.columns})

    # override
    def addSuccess(self, test):
        row_key = self._row_key_from_test(test)
        self.stats[row_key]['success'] += 1

    # override
    def addError(self, test, err, capt=None):
        row_key = self._row_key_from_test(test)
        self.stats[row_key]['error'] += 1

    # override
    def addFailure(self, test, err, capt=None):
        row_key = self._row_key_from_test(test)
        self.stats[row_key]['failure'] += 1

    # override
    def addDeprecated(self, test, err, capt=None):
        row_key = self._row_key_from_test(test)
        self.stats[row_key]['deprecated'] += 1

    # override
    def addSkip(self, test, err, capt=None):
        row_key = self._row_key_from_test(test)
        self.stats[row_key]['skip'] += 1

    # override
    def report(self, stream):
        non_empty_columns = [status for status in self.columns if any(self.stats[key][status] for key in self.stats)]
        max_col_len = max(len(status) for status in non_empty_columns)
        max_key_len = max(len(key or '') for key in self.stats.keys())
        header_format = '{:>' + str(max_key_len) + '}' + (' | {:' + str(max_col_len) + '}') * len(non_empty_columns)
        row_format = '{row_key:>' + str(max_key_len) + '} | ' + ' | '.join('{' + status + ':' + str(max_col_len) + '}' for status in non_empty_columns)
        stream.writeln('-' * 70)
        stream.writeln('Summary:')
        stream.writeln(header_format.format(self.summary_report_on, *non_empty_columns))
        stream.writeln('   ' + '-' * (max_key_len + len(non_empty_columns) * (max_col_len + 3)))
        for row_key, stats in self.stats.items():
            if row_key:  # can be None
                stats['row_key'] = row_key
                stream.writeln(row_format.format(**stats))

    def _row_key_from_test(self, test):
        class_name = None
        if hasattr(test, 'address'):
            _, path, method = test.address()
            if method and '.' in method:
                class_name, method = method.split('.')
        elif ' context=' in test.id() and test.id().count(':') == 1:
            bracketed, method = test.id().split(':', 1)
            path, class_name = bracketed[1:-1].split(' context=', 1)
        else:
            path, class_name, method = test.id().rsplit('.', 2)
            if class_name[0].islower():
                path += '.' + class_name
                class_name = None
        return {
            'module-path': path,
            'top-module': path.split('.', 1)[0],
            'class': class_name
        }[self.summary_report_on]