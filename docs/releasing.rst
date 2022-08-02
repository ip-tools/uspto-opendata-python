#######################
Releasing this software
#######################

Cut a release
=============
::

    make release bump=minor


Build package
=============
::

    # Build sdist package
    python setup.py sdist


Upload to PyPI
==============
::

    # Test upload
    twine upload --repository testpypi dist/*

    # Real upload
    twine upload dist/uspto-opendata-python-0.5.2.tar.gz

See also: https://pypi.python.org/pypi/twine
