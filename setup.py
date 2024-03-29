#!/usr/bin/env python

from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as f:
    description = f.read()

about = {}
with open('django_global_places/__version__.py', 'r', encoding="utf8") as f:
    exec(f.read(), about)

setup(
    name='django_global_places',
    version=about['__version__'],
    author='lucacitta',
    author_email='lucacitta.dev@gmail.com',
    url='https://github.com/lucacitta/Django-GlobalPlaces',
    description='Django Global Places is a simple Django app to provide a model for global places.',
    license='MIT',
    packages=find_packages(),
    long_description=description,
    long_description_content_type='text/markdown',
    keywords='django global places',
    zip_safe=False,
    install_requires=[
        'Django>=3.8.0',
        'pandas>=2.2.0',
        'requests>=2.30'
    ],
    include_package_data=True,
    python_requires='>=3.8',
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
