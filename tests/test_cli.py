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


from lxml import etree
import py.path
import pytest
from unittest.mock import patch

import schvalidator
from schvalidator.cli import parsecli
from schvalidator.common import ERROR_CODES
from schvalidator.exceptions import ProjectFilesNotFoundError

TESTDIR = py.path.local(__file__).dirpath()
DATADIR = TESTDIR / "data"


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


def test_main_mock_parsecli(monkeypatch):
    """ """
    def mock_parsecli(cliargs=None):
        return {'--schema': None,
                'XMLFILE':  None,
                }

    monkeypatch.setattr(schvalidator.cli,
                        'parsecli',
                        mock_parsecli)

    result = schvalidator.cli.main()
    assert result == ERROR_CODES[ProjectFilesNotFoundError]


def test_main_mock_parsecli_process(monkeypatch):
    """ """
    def mock_parsecli(cliargs=None):
        return {'--schema': "s.sch",
                '--phase': None,
                'XMLFILE':  "a.xml",
                }
    def mock_process(args):
        # Use a return code that is never be used in schvalidator:
        return -1

    monkeypatch.setattr(schvalidator.cli,
                        'parsecli',
                        mock_parsecli)
    monkeypatch.setattr(schvalidator.cli,
                        'process',
                        mock_process)
    assert schvalidator.cli.main() == -1


@pytest.mark.parametrize("excpt,data", [
    (etree.XMLSyntaxError, ["msg", "x", 1, 1]),
    (etree.XSLTApplyError, ["msg"]),
])
def test_main_raise_etree(monkeypatch, excpt, data):
    """ """
    def mock_parsecli(cliargs=None):
        return {'--schema': "s.sch",
                '--phase': None,
                'XMLFILE':  "a.xml",
                }
    def mock_process(args):
        raise excpt(*data)

    monkeypatch.setattr(schvalidator.cli,
                        'parsecli',
                        mock_parsecli)
    monkeypatch.setattr(schvalidator.schematron,
                        'process',
                        mock_process)

    result = schvalidator.cli.main()
    #  == ERROR_CODES[excpt]
    assert result


@pytest.mark.parametrize("excpt", [
    FileNotFoundError, OSError,
])
def test_main_raise_OSError(monkeypatch, excpt):
    def mock_parsecli(cliargs=None):
        return {'--schema': "s.sch",
                '--phase': None,
                'XMLFILE':  "a.xml",
                }
    def mock_process(args):
        raise excpt()

    monkeypatch.setattr(schvalidator.cli,
                        'parsecli',
                        mock_parsecli)
    monkeypatch.setattr(schvalidator.schematron,
                        'process',
                        mock_process)

    result = schvalidator.cli.main()
    assert result == ERROR_CODES[excpt]
