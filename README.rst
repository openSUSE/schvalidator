Validate XML Files with ISO Schematron Schemas
**********************************************

License: GPL 3+

.. image:: https://travis-ci.org/openSUSE/schvalidator.svg?branch=develop
    :target: https://travis-ci.org/openSUSE/schvalidator
    :alt: Travis CI
.. image:: https://codeclimate.com/github/openSUSE/schvalidator/badges/gpa.svg
    :target: https://codeclimate.com/github/openSUSE/schvalidator
    :alt: Code Climate
.. image:: https://scrutinizer-ci.com/g/openSUSE/schvalidator/badges/quality-score.png?b=develop
    :target: https://scrutinizer-ci.com/g/openSUSE/schvalidator/?branch=develop
    :alt: Scrutinizer Code Quality
.. image:: https://codecov.io/github/openSUSE/schvalidator/coverage.svg?branch=develop
    :target: https://codecov.io/github/openSUSE/schvalidator?branch=develop
    :alt: Code Coverage

The :program:`schvalidator` script validates a given XML file with a
`ISO Schematron schema <https://en.wikipedia.org/wiki/Schematron>`_.
Older Schematron versions are not supported.


Quick Start
===========

To use the program without :command:`pip` and virtual environment, use the
following command after cloning this repository::

    $ PYTHONPATH=src python3 -m schvalidator -h


Installation
============

To install :program:`schvalidator`, use the following steps:

#. Clone this repository::

    $ git clone http://github.com/openSUSE/schvalidator.git
    $ cd schvalidator

#. Create a Python 3 environment and activate it::

    $ pyvenv .env
    $ source .env/bin/activate

#. Update the ``pip`` and ``setuptools`` modules::

    $ pip install -U pip setuptools

#. Install the package::

    $ ./setup.py develop

If you need to install it from GitHub directly, use this URL::

    git+https://github.com/openSUSE/schvalidator.git@develop

After the installation in your Python virtual environment, the script
:program:`schvalidator` is available.


Workflow
========

The script does the following steps:

#. Collect all options and arguments through the docopts library.

#. Check, if a Schematron schema and a XML file is passed to the script
   and they are available.

#. If everything is ok, create a Schematron validator with the lxml
   library and validate the XML file.

#. Get the result of the validation in an XML report with the root element
   ``svrl:schematron-output`` created by lxml.

#. Iterate through all ``svrl:failed-assert`` elements and output them
   accordingly. Take into account the ``role`` attribute and map them
   to the logging level.

Done!


Contributing
============

To contribute to this project, open issues or send us pull requests. Thanks!
