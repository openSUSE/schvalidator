#
# Copyright (c) 2016 SUSE Linux GmbH
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 3 of the GNU General Public License as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, contact SUSE LLC.
#
# To contact SUSE about this file by physical or electronic mail,
# you may find current contact information at www.suse.com

import os.path
from lxml import etree
import pytest
import sys
from unittest.mock import Mock

import schvalidator.schematron
from schvalidator.schematron import (NS, NSElement,
                                     extractrole,
                                     process,
                                     svrl, validate_sch)


@pytest.mark.parametrize('validation_result,return_value', [
    (True,  0),
    (False, 200),
])
def test_process(monkeypatch, validation_result, return_value, tmpdir):
    """Test process() function"""
    args = {'--schema': None,
            'XMLFILE':  None,
            '--phase':  None,
            '--report': str(tmpdir / "report.svrl"),
            }
    def mockreturn(schema, xmlfile, phase=None, xmlparser=None):
        mock = Mock()
        mock.validation_report = etree.XML("<root/>").getroottree()
        return validation_result, mock

    monkeypatch.setattr(schvalidator.schematron,
                        'check_args',
                        lambda x: None)
    monkeypatch.setattr(schvalidator.schematron,
                        'validate_sch',
                        mockreturn)

    assert process(args) == return_value


@pytest.mark.parametrize('role', [
    # (parent, failed-assert, expected)
    (None, None, None),
    ('info', None, 'info'),
    (None, 'info', 'info'),
    ('info', 'error', 'error'),
])
def test_extractrole(role):
    """ """
    def roleattr(value):
        if value:
            return 'role=%r' % value
        return ''

    parent, current, expected = role
    xmltree = etree.XML("""<svrl:schematron-output
    xmlns:svrl="http://purl.oclc.org/dsdl/svrl">
  <svrl:ns-prefix-in-attribute-values
        uri="http://docbook.org/ns/docbook" prefix="d"/>
  <svrl:active-pattern id="all.general" name="General Rules"/>
  <svrl:fired-rule context="/*" %s/>
  <svrl:failed-assert %s
    test="@version = '5.0'"
    location="/*[local-name()='article' and namespace-uri()='http://docbook.org/ns/docbook']">
    <svrl:text>bla</svrl:text>
  </svrl:failed-assert>
</svrl:schematron-output>
    """ % (roleattr(parent),
           roleattr(current)))

    fa = list(xmltree.iter(svrl("failed-assert").text))[0]
    resultrole = extractrole(fa)
    assert resultrole == expected


def test_extractrole_empty():
    xmltree = etree.XML("""<svrl:schematron-output
    xmlns:svrl="http://purl.oclc.org/dsdl/svrl">
   <svrl:failed-assert
    test="@version = '5.0'"
    location="/*[local-name()='article' and namespace-uri()='http://docbook.org/ns/docbook']">
    <svrl:text>bla</svrl:text>
  </svrl:failed-assert>
</svrl:schematron-output>""")
    fa = list(xmltree.iter(svrl("failed-assert").text))[0]
    resultrole = extractrole(fa)
    assert resultrole is None


def test_process_result_svrl(caplog):

    process_result_svrl(xmltree)


def test_NSElement():
    foo = etree.QName("ns", "foo")
    element = NSElement("ns")
    assert element.prefix is None
    assert element.ns == "ns"
    assert repr(element) == "NSElement(ns)"
    assert element("foo") == foo
    assert element.foo == foo
