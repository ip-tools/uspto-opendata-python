import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    'celery==4.1.0',
    'requests==2.18.4',
    'redis==2.10.6',
    'beautifulsoup4==4.6.0',
    'docopt==0.6.2',
    'pathvalidate==0.16.2',
    'lxml==4.2.5',
    'jsonpointer==1.12',
    'clint==0.5.1',
    'awesome-slugify==1.6.5',
]

test_requires = [
]

setup(name='uspto-opendata-python',
      version='0.8.0',
      description='uspto-opendata-python is a client library for accessing the USPTO Open Data APIs',
      long_description=README,
      license="MIT",
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Legal Industry",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Archiving",
        "Topic :: Text Processing",
        "Topic :: Utilities",
      ],
      author='Andreas Motl',
      author_email='andreas.motl@ip-tools.org',
      url='https://github.com/ip-tools/uspto-opendata-python',
      keywords='uspto pair pbd peds opendata bulk data download patent information research search',
      packages=find_packages(),
      include_package_data=True,
      package_data={
      },
      zip_safe=False,
      test_suite='nose.collector',
      install_requires=requires,
      tests_require=test_requires,
      extras_require={
          'release': [
              'bumpversion==0.5.3',
              'twine==1.9.1',
              'keyring==10.4.0',
          ],
          'documentation': [
              'Sphinx==1.6.4',
              'sphinx_rtd_theme==0.2.5b1',
          ],
      },
      dependency_links=[
        'https://github.com/kennethreitz/clint/tarball/9d3693d6#egg=clint-0.5.1',
      ],

      entry_points={
        'console_scripts': [
            'uspto-pbd  = uspto.pbd.command:run',
            'uspto-peds = uspto.peds.command:run',
        ],
      },

    )
