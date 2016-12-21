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

from schvalidator.log import setloglevel
import schvalidator.schematron
from schvalidator.schematron import (NS, NSElement,
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



def test_xml(schtestcase):
    """Run one test case"""
    xmlfile, schema, svrl = schtestcase
    setloglevel(logging.NOTSET)

    result, schematron = validate_sch(str(schema), str(xmlfile))
    report = schematron.validation_report
    svrltree = etree.parse(str(svrl))

    xpathexpr = ["count(//svrl:failed-assert)"]
    for expr in xpathexpr:
        expected = svrltree.xpath(expr, namespaces=NS)
        result = report.xpath(expr, namespaces=NS)
        assert expected == result


def test_NSElement():
    foo = etree.QName("ns", "foo")
    element = NSElement("ns")
    assert element.prefix is None
    assert element.ns == "ns"
    assert repr(element) == "NSElement(ns)"
    assert element("foo") == foo
    assert element.foo == foo
