#!/usr/bin/env python

import os

from setuptools import find_packages, setup

here = os.path.dirname(os.path.abspath(__file__))
# f = open(os.path.join(here, 'README.md'))
# long_description = f.read().strip()
# f.close()


about = {}
with open('django_global_places/__version__.py', 'r', encoding="utf8") as f:
    exec(f.read(), about)

setup(
    name='Django Global Places',
    version=about['__version__'],
    author='lucacitta',
    author_email='lucacitta.dev@gmail.com',
    url='https://github.com/lucacitta/Django-GlobalPlaces',
    description='Django Global Places is a simple Django app to provide a model for global places.',
    license='MIT',
    packages=find_packages(),
    # long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='django global places',
    zip_safe=False,
    install_requires=[
        'Django>=3.8.0',
        'djangorestframework>=3.13.0',
    ],
    extras_require={
        'with_social': ['django-allauth>=0.56.0,<0.58.0'],
    },
    tests_require=[
        'coveralls>=1.11.1',
        'django-allauth>=0.57.0',
        'djangorestframework-simplejwt==4.6.0',
        'responses==0.12.1',
        'unittest-xml-reporting==3.6.1',
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
