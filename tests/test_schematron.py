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

from schvalidator import log
from schvalidator.log import logging
import schvalidator.schematron
from schvalidator.schematron import (NS, NSElement,
                                     extractrole,
                                     process, process_result_svrl,
                                     svrl, validate_sch)


def test_NSElement():
    foo = etree.QName("ns", "foo")
    element = NSElement("ns")
    assert element.prefix is None
    assert element.ns == "ns"
    assert repr(element) == "NSElement(ns)"
    assert element("foo") == foo
    assert element.foo == foo


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
    xmltree = etree.XML("""<svrl:schematron-output
    xmlns:svrl="http://purl.oclc.org/dsdl/svrl">
   <svrl:failed-assert role="info"
    test="@version = '5.0'"
    location="/*[local-name()='article' and namespace-uri()='http://docbook.org/ns/docbook']">
    <svrl:text>bla</svrl:text>
  </svrl:failed-assert>
</svrl:schematron-output>""")

    process_result_svrl(xmltree)
    assert caplog.text
    for record in caplog.records:
        assert record.levelname == 'INFO'
        assert record.name == 'schematron'
        assert record.getMessage()
        assert record.funcName == process_result_svrl.__name__


@pytest.mark.parametrize('xmlparser', [
    None, "xmlparser"
])
def test_validate_sch(monkeypatch, xmlparser):
    def mock_etree_parse(source, parser=None, *, base_url=None):
        return Mock()
    def mock_schematron(etree=None, file=None,
                        include=True, expand=True, include_params={}, expand_params={}, compile_params={}, store_schematron=False, store_xslt=False, store_report=False, phase=None,
                        error_finder=None):
        mock = Mock()
        mock.validate.return_value = True
        return mock

    monkeypatch.setattr(schvalidator.schematron.etree,
                        'parse',
                        mock_etree_parse)
    monkeypatch.setattr(schvalidator.schematron,
                        'Schematron',
                        mock_schematron)
    result, schematron = validate_sch("fake.sch",
                                      "fake.xml",
                                      xmlparser=xmlparser)
    assert result
    assert getattr(schematron, 'validate')
