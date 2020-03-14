[![pypi\_version\_img](https://img.shields.io/pypi/v/nose-summary-report.svg?style=flat)](https://pypi.python.org/pypi/nose-summary-report) [![Supported Python versions](https://img.shields.io/pypi/pyversions/nose-summary-report.svg)](https://pypi.python.org/pypi/nose-summary-report) [![pypi\_license\_img](https://img.shields.io/pypi/l/nose-summary-report.svg?style=flat)](https://pypi.python.org/pypi/nose-summary-report) [![travis\_build\_status](https://travis-ci.org/Lucas-C/nose-summary-report.svg?branch=master)](https://travis-ci.org/Lucas-C/nose-summary-report)

# summary-report

A very basic [nose](https://nose.readthedocs.io/en/latest/) plugin providing a per-module tests status final report.

Example output for [pelican-plugins](https://github.com/getpelican/pelican-plugins) tests:
```
----------------------------------------------------------------------
Summary:
         top-module | success | error   | failure
   -------------------------------------------------
    collate_content |       8 |       0 |       0
      disqus_static |       0 |       1 |       0
   filetime_from_hg |       0 |       1 |       0
         gzip_cache |       3 |       1 |       1
      i18n_subsites |       8 |       0 |       1
      image_process |       1 |       4 |       1
        jpeg_reader |       0 |       2 |       0
         libravatar |       0 |       1 |       0
        liquid_tags |       0 |       7 |       0
    more_categories |       3 |       0 |       0
    multi_neighbors |       0 |       1 |       0
  org_python_reader |       0 |       1 |       0
                pdf |       0 |       1 |       0
pelican_unity_webgl |       0 |       1 |       0
               nose |       0 |       4 |       0
         post_stats |       0 |       2 |       0
      reddit_poster |       0 |       1 |       0
      similar_posts |       0 |       1 |       0
   simple_footnotes |       1 |       0 |       1
            summary |       4 |       0 |       0
        thumbnailer |       0 |       1 |       0
----------------------------------------------------------------------
Ran 66 tests in 10.188s

FAILED (SKIP=9, errors=29, failures=4)
```

## Usage

    pip install nose-summary-report
    nosetests --with-summary-report

You can choose other ways to aggregate the tests status:

    nosetests --with-summary-report --summary-report-on class
    nosetests --with-summary-report --summary-report-on module-path

## Development
### Releasing a new version
With a valid `~/.pypirc`:

1. edit version in `setup.py`
2. `python setup.py sdist`
3. `twine upload dist/*`
4. `git tag $version && git push && git push --tags`

