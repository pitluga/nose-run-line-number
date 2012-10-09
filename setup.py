from setuptools import setup

setup(
    name = "nose-run-line-number",
    version = '0.0.1',
    description = "Nose plugin to run tests by line number",
    long_description = "Nose plugin to run tests by line number",
    url = "https://github.com/pitluga/nose-run-line-number",
    author = "Tony Pitluga",
    author_email = "tony.pitluga@gmail.com",
    license = "MIT",

    packages = ["nose_run_line_number"],
    scripts = ["bin/noseline"],
    entry_points = {
        'nose.plugins.0.10': [
            'nose_run_line_number = nose_run_line_number:RunLineNumber'
            ]
        },
)
