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

from schvalidator.log import setloglevel
from schvalidator.schematron import (NS, NSElement,
                                     svrl, validate_sch)


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
