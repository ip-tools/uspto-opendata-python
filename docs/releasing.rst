#######################
Releasing this software
#######################

Setup prerequisites
===================
::

    pip install -e .[release]


Cut a release
=============
::

    make release bump=minor


Build package
=============
::

    # flit build
    python setup.py sdist


Upload to PyPI
==============
::

    # Test upload
    flit --repository testpypi publish --format sdist

    # Real upload
    flit --repository pypi publish --format sdist

See also: https://flit.readthedocs.io/
