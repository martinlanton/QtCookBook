from setuptools import setup, find_packages

name = 'QtCookBook'
author = "Martin L'Anton"
author_email = "lantonmartin@gmail.com"
url = "https://github.com/martinlanton/QtCookBook"

setup(
    name=name,
    version='0.1.0',
    author=author,
    author_email=author_email,
    url=url,
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'pytest-cov',
        'PySide6',
    ]
)
