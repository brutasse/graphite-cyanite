# coding: utf-8
from setuptools import setup

setup(
    name='cyanite',
    version='0.4.6',
    url='https://github.com/brutasse/graphite-cyanite',
    license='BSD',
    author=u'Bruno Renié',
    author_email='bruno@renie.fr',
    description=('A plugin for using graphite-web with the cassandra-based '
                 'Cyanite storage backend'),
    long_description=open('README.rst').read(),
    py_modules=('cyanite',),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    classifiers=(
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: System :: Monitoring',
    ),
    install_requires=(
        'requests',
    ),
    test_suite='tests',
)
