"""Setup for gherkin_question XBlock."""

import os
from setuptools import setup


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='simple-excel-xblock',
    version='0.1',
    description='Very Simple Excel XBlock',   # TODO: write a better description.
    license='AGPL v3',          # TODO: choose a license: 'AGPL v3' and 'Apache 2.0' are popular.
    packages=[
        'simple_excel',
    ],
    install_requires=[
        'XBlock',
        'jinja2',
    ],
    entry_points={
        'xblock.v1': [
            'simple_excel = simple_excel:SimpleExcelXBlock',
        ]
    },
    package_data=package_data("simple_excel", ["public", "templates", "migrations"]),
)
