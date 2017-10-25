#################
Python virtualenv
#################

About
=====
virtualenv_ is a tool to create isolated Python environments.
We recommend it for installing the software and its dependencies
independently of your Python distribution.


Install
=======

Create Python virtualenv::

    # Either use Python 2.7 ...
    virtualenv --no-site-packages .venv27

    # ... or Python 3.6
    virtualenv --no-site-packages --python python3.6 .venv36

Install::

    # Activate virtualenv
    source .venv27/bin/activate

    # or
    source .venv36/bin/activate

    # Install Python package
    pip install uspto-opendata-python


.. _virtualenv: https://virtualenv.pypa.io/

