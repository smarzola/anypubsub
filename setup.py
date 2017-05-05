from setuptools import setup, find_packages
import sys, os, multiprocessing

requires = ['six']

py_version = sys.version_info[:2]

PY3 = py_version[0] == 3

if PY3:
    if py_version < (3, 3):
        raise RuntimeError('On Python 3, anypubsub requires Python 3.3 or better')
else:
    if py_version < (2, 7):
        raise RuntimeError('On Python 2, anypubsub requires Python 2.7 or better')

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''

setup(
    name='anypubsub',
    version='0.6',
    description="A generic interface wrapping multiple backends to provide a consistent pubsub API.",
    long_description=README,
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='pubsub pub/sub redis mongodb',
    author='Simone Marzola',
    author_email='marzolasimone@gmail.com',
    url='http://github.com/simock85/anypubsub',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require={
        'redis': [
            'redis > 2.10',
        ],
        'mongodb': [
            'pymongo >= 3',
        ],
        'amqp': [
            'amqp >= 1.4.9'
        ]
    },
    test_suite='nose.collector',
    tests_require = [
        'nose',
        'mock',
        'coverage',
        'redis > 2.10',
        'pymongo >= 3',
        'amqp >= 1.4.9',
    ],
    entry_points="""\
    """,
)
