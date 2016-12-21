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


import pytest
from unittest.mock import patch

from schvalidator.cli import parsecli


@pytest.mark.parametrize('cli,expected', [
  (['--schema', 'schema.sch', 'a.xml'],
   {'--schema': 'schema.sch',
    'XMLFILE':  'a.xml'}
   ),
  (['-v', '--schema', 'schema.sch', 'a.xml'],
   {'-v': 1,
    '--schema': 'schema.sch',
    'XMLFILE':  'a.xml'}
   ),
  (['-vv', '--schema', 'schema.sch', 'a.xml'],
   {'-v': 2,
    '--schema': 'schema.sch',
    'XMLFILE':  'a.xml'}
   ),
  (['-vvv', '--schema', 'schema.sch', 'a.xml'],
   {'-v': 3,
    '--schema': 'schema.sch',
    'XMLFILE':  'a.xml'}
   ),
  (['--report', 'report.svrl', '--schema', 'schema.sch', 'a.xml'],
   {'--report': 'report.svrl',
    '--schema': 'schema.sch',
    'XMLFILE':  'a.xml'}
   ),
   (['--phase', 'foo', '--schema', 'schema.sch', 'a.xml'],
   {'--phase': 'foo',
    '--schema': 'schema.sch',
    'XMLFILE':  'a.xml'}
   ),
])
def test_parsecli(cli, expected):
    result = parsecli(cli)
    # Create set difference and only compare this with the expected dictionary
    assert {item: result.get(item, None) for item in expected} == expected
