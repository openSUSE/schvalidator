.. schvalidator documentation master file

:orphan:

schvalidator -- Manual Page
===========================


Synopsis
--------
::

 schvalidator [OPTIONS] --schema SCHEMA XMLFILE


Description
-----------

:program:`schvalidator` expects a `ISO Schematron schema
<https://en.wikipedia.org/wiki/Schematron>`_
and a XML file to validate. If there are validation errors, the script
reports each error in a separate line.


Conceptual Overview
-------------------

Basically, before a Schematron schema can perform its validation task,
it is internally transformed into a XSLT stylesheet by the lxml library.
This *in-memory stylesheet* is then applied to the XML file.

This stylesheet creates a *validation report* as an XML file.
The root element ``svrl:schematron-output`` belongs to the namespace
``http://purl.oclc.org/dsdl/svrl`` (see below). The validation report
contains all failed assertions and their error messages. The "severity" of
the assertion is stored in the ``role`` attribute (if available). To
get this validation report, use the option :option:`--report` to save
it to a file.


Options
-------

.. program:: schvalidator

.. option:: -h, --help

   Display usage summary

.. option:: --version

   Prints the version

.. option:: -v...

   Raise verbosity level; can be used more than once

.. option:: --report <REPORTFILE>

   Save output of Schematron validation to REPORTFILE

.. option:: --phase <PHASE>

   Set a validation phase

.. option:: --schema <SCHEMA>

   Points to the Schematron file

.. option:: XMLFILE

   Path to the XML file to validate


Example
-------

Let's assume we have the following ISO Schematron schema in :file:`root.sch`.
The Schematron schema checks if the root element contains a ``version``
and a ``xml:id`` attribute. If one or both are not available it prints
the error message inside the ``sch:assert`` element.

.. sourcecode:: xml

    <sch:schema id="schematron-001.sch" queryBinding="xslt"
                xmlns:d="http://docbook.org/ns/docbook"
                xmlns:sch="http://purl.oclc.org/dsdl/schematron">
        <sch:pattern>
            <sch:title>Rules</sch:title>
            <sch:rule context="/*">
            <sch:assert test="@version and @xml:id">
                Root element needs @version and @xml:id attributes!
            </sch:assert>
            </sch:rule>
        </sch:pattern>
    </sch:schema>


Your DocBook 5 source is saved in file :file:`article.xml`:

.. sourcecode:: xml

    <article xml:id="article"
             xmlns="http://docbook.org/ns/docbook"
             xmlns:xlink="http://www.w3.org/1999/xlink">
       <title>Article Validated with Schematron</title>
       <para>bla</para>
    </article>

Run the script :program:`schvalidator` like this::

    $ schvalidator --schema root.sch article.xml

it gives you the following output::

    [INFO]: No. 1
        Location: "/*[local-name()='article' and namespace-uri()='http://docbook.org/ns/docbook']"
        Message: Root element needs @version and @xml:id attributes!
    --------------------
    [CRITICAL]: Validation failed!

If the :option:`--report` option is used, you can save the
resulting validation report to a file. In this case, the validation
report contains the following elements:

.. sourcecode:: xml

    <svrl:schematron-output schemaVersion="" title="root.sch"
        xmlns:iso="http://purl.oclc.org/dsdl/schematron"
        xmlns:sch="http://www.ascc.net/xml/schematron"
        xmlns:schold="http://www.ascc.net/xml/schematron"
        xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
        xmlns:xs="http://www.w3.org/2001/XMLSchema">
        <svrl:active-pattern name="Rules"/>
        <svrl:fired-rule context="/*"/>
        <svrl:failed-assert
            location="/*[local-name()='article' and namespace-uri()='http://docbook.org/ns/docbook']"
            test="@version and @xml:id">
            <svrl:text> Root element needs @version and @xml:id attributes!
            </svrl:text>
        </svrl:failed-assert>
    </svrl:schematron-output>



Diagnostics
-----------

:program:`schvalidator` return codes provide information
that can be used when calling it from scripts.

+-----+----------------------------------------------+
| 0   | no error                                     |
+-----+----------------------------------------------+
| 10  | no Schematron schema or XML file found       |
+-----+----------------------------------------------+
| 20  | XML or Schematron error                      |
+-----+----------------------------------------------+
| 30  | file not found or general OS error           |
+-----+----------------------------------------------+
| 200 | validation failed                            |
+-----+----------------------------------------------+

See also
--------

:manpage:`jing(1)`, :manpage:`xmllint(1)`


Author
------

   Thomas Schraitle <toms(AT)opensuse.org>
