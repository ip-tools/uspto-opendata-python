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

    flit --repository testpypi publish

See also: https://flit.readthedocs.io/
