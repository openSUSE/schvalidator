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
import logging
from lxml import etree
import pytest
import sys
from unittest.mock import Mock

import schvalidator.schematron
from schvalidator.schematron import (NSElement,
                                     extractrole,
                                     process, process_result_svrl,
                                     svrl, validate_sch)
from schvalidator.common import NSMAP


def test_NSElement():
    foo = etree.QName("ns", "foo")
    element = NSElement("ns")
    assert element.prefix is None
    assert element.ns == "ns"
    assert repr(element) == "NSElement(ns)"
    assert element("foo") == foo
    assert element.foo == foo


@pytest.mark.parametrize('reportfile', [
    None, "report.svrl"
])
@pytest.mark.parametrize('validation_result,return_value', [
    (True,  0),
    (False, 200),
])
def test_process(monkeypatch, tmpdir,
                 validation_result, return_value, reportfile):
    """Test process() function"""
    args = {'SCHEMA': None,
            'XMLFILE':  None,
            '--phase':  None,
            '--store-xslt': None,
            '--report': str(tmpdir / reportfile) \
                        if reportfile is not None else None
            }
    def mockreturn(schema, xmlfile, phase=None, xmlparser=None):
        mock = Mock()
        mock.validation_report = etree.XML("<root/>").getroottree()
        return validation_result, mock

    monkeypatch.setattr(schvalidator.schematron,
                        'validate_sch',
                        mockreturn)

    assert process(args) == return_value


@pytest.mark.parametrize('xsltfile', [None, "result.xslt"])
def test_process_store_xslt(monkeypatch, tmpdir,
                            xsltfile):
    args = {'SCHEMA': None,
            'XMLFILE':  None,
            '--phase':  None,
            '--report': None,
            '--store-xslt': str(tmpdir / xsltfile) \
                            if xsltfile is not None else None
            }
    def mockreturn(schema, xmlfile, phase=None, xmlparser=None):
        mock = Mock()
        mock.validation_report = etree.XML("""<svrl:schematron-output
            xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
            schemaVersion="" title="None"/>""").getroottree()
        mock.validator_xslt = etree.XML("""<xsl:stylesheet
            version="1.0"
            xmlns:xsl="http://www.w3.org/1999/XSL/Transform"/>""").getroottree()
        return True, mock

    monkeypatch.setattr(schvalidator.schematron,
                        'validate_sch',
                        mockreturn)
    assert process(args) == 0
    if args['--store-xslt'] is not None:
        assert os.path.exists(args['--store-xslt'])


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

    log = logging.getLogger(schvalidator.__package__)
    log.setLevel(logging.INFO)
    process_result_svrl(xmltree)
    # assert caplog.text
    for record in caplog.records:
        assert record.levelname == 'INFO'
        assert record.name == schvalidator.__package__
        assert record.getMessage()
        assert record.funcName == process_result_svrl.__name__


# @pytest.mark.skip
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
    monkeypatch.setattr(schvalidator.schematron,
                        'check4schematron',
                        lambda x, y: None
                        )
    result, schematron = validate_sch("fake.sch",
                                      "fake.xml",
                                      xmlparser=xmlparser)
    assert result
    assert getattr(schematron, 'validate')
