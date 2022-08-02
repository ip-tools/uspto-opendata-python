import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    'celery<5',
    'requests<3',
    'redis<3',
    'beautifulsoup4<5',
    'docopt<1',
    'pathvalidate<1',
    'lxml<5',
    'jsonpointer<2',
    'clint==0.5.1',
    'awesome-slugify<2',
]

test_requires = [
]

setup(name='uspto-opendata-python',
      version='0.8.3',
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
      test_suite='nose2.collector.collector',
      install_requires=requires,
      tests_require=test_requires,
      extras_require={
          'test': [
              'nose2',
          ],
      },
      dependency_links=[
        'https://github.com/kennethreitz-archive/clint/tarball/9d3693d6#egg=clint-0.5.1',
      ],

      entry_points={
        'console_scripts': [
            'uspto-pbd  = uspto.pbd.command:run',
            'uspto-peds = uspto.peds.command:run',
        ],
      },

    )
