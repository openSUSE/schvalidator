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

from lxml.etree import XSLTParseError
import pytest
import schvalidator
from schvalidator.common import ERROR_CODES


SCHEMATRON="""<sch:schema id="schematron-003.sch" queryBinding="xslt"
  xmlns:d="http://docbook.org/ns/docbook"
  xmlns:sch="http://purl.oclc.org/dsdl/schematron">

  <!-- Missing sch:ns -->
  <!-- <sch:ns prefix="d" uri="http://docbook.org/ns/docbook"/> -->

  <sch:pattern>
    <sch:title>Rule</sch:title>
    <sch:rule context="/d:article">
      <sch:assert test="@xml:id">
        Expected an xml:id attribute
      </sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>
"""

XML="""<article version="5.1"/>"""


def test_use_wrong_schematron(tmpdir):
    schemafile = tmpdir / "schema.sch"
    xmlfile = tmpdir / "article.xml"
    schemafile.write(SCHEMATRON)
    xmlfile.write(XML)

    result = schvalidator.main(['--schema', str(schemafile),
                           str(xmlfile)])
    assert result == ERROR_CODES.get(repr(XSLTParseError))
