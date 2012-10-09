A plugin to run nose tests by line number.

## To install

It's available on PyPi, so its as simple as:

```
pip install nose-run-line-number
```

## To Run

If you are building your project with ```setuptools``` you will just need to include it in ```test_require```. Then you can run it from the command line line so:

```python setup.py nosetests --line-file tests/folder/file_test.py --line 7```

If you are not using ```setuptools```, nose-run-line-number ships with an executable that will plug itself into nosetests

```noseline tests/folder/file_test.py --line 7```