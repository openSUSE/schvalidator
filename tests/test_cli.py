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
from schvalidator.common import ERROR_CODES, errorcode
from schvalidator.exceptions import (NoISOSchematronFileError,
                                     OldSchematronError,
                                     ProjectFilesNotFoundError,
                                     )

TESTDIR = py.path.local(__file__).dirpath()
DATADIR = TESTDIR / "data"


def test_errorcode():
    for error in ERROR_CODES:
        assert errorcode(error)


def test_invalid_errorcode():
    assert errorcode(ArithmeticError) == 255


@pytest.mark.parametrize('cli,expected', [
  ([ 'schema.sch', 'a.xml'],
   {'SCHEMA': 'schema.sch',
    'XMLFILE':  'a.xml'}
   ),
  (['-v', 'schema.sch', 'a.xml'],
   {'-v': 1,
    'SCHEMA': 'schema.sch',
    'XMLFILE':  'a.xml'}
   ),
  (['-vv', 'schema.sch', 'a.xml'],
   {'-v': 2,
    'SCHEMA': 'schema.sch',
    'XMLFILE':  'a.xml'}
   ),
  (['-vvv', 'schema.sch', 'a.xml'],
   {'-v': 3,
    'SCHEMA': 'schema.sch',
    'XMLFILE':  'a.xml'}
   ),
  (['--report', 'report.svrl', 'schema.sch', 'a.xml'],
   {'--report': 'report.svrl',
    'SCHEMA': 'schema.sch',
    'XMLFILE':  'a.xml'}
   ),
   (['--phase', 'foo', 'schema.sch', 'a.xml'],
   {'--phase': 'foo',
    'SCHEMA': 'schema.sch',
    'XMLFILE':  'a.xml'}
   ),
   (['--phase', 'foo', '--report', 'report.svrl',
     'schema.sch', 'a.xml'],
   {'--phase': 'foo',
    '--report': 'report.svrl',
    'SCHEMA': 'schema.sch',
    'XMLFILE':  'a.xml'}
   ),
   (['--store-xslt', 'foo.xsl', 'schema.sch', 'a.xml'],
    {'--store-xslt': 'foo.xsl',
     'SCHEMA': 'schema.sch',
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
        return {'SCHEMA': None,
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
        return {'SCHEMA': "s.sch",
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


@patch('schvalidator.cli.process')
@patch('schvalidator.cli.parsecli')
@patch('schvalidator.cli.check_files')
@pytest.mark.parametrize("excpt,data", [
    (etree.XMLSyntaxError, ["msg", "x", 1, 1]),
    (etree.XSLTApplyError, ["msg"]),
])
def test_main_raise_etree(mock_check_files, mock_parsecli, mock_process,
                           excpt, data,):
    mock_parsecli.return_value = None
    mock_check_files.return_value = None
    mock_process.side_effect = excpt(*data)
    result = schvalidator.cli.main()

    assert result == ERROR_CODES[excpt]


@pytest.mark.parametrize("excpt", [
    FileNotFoundError, OSError,
])
def test_main_raise_OSError(monkeypatch, excpt):
    def mock_parsecli(cliargs=None):
        return {'SCHEMA': "s.sch",
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



def test_oldschematron(monkeypatch):

    def _parsecli(cliargs=None):
        return {'SCHEMA': str(DATADIR / "old-schematron.sch"),
                'XMLFILE': str(DATADIR / "article-001.xml"),
                '--phase': None,
                }
    monkeypatch.setattr(schvalidator.cli,
                        'parsecli',
                        _parsecli)

    result = schvalidator.cli.main()
    assert result == ERROR_CODES[OldSchematronError]


def test_isoschematron(monkeypatch):

    def _parsecli(cliargs=None):
        return {'SCHEMA': str(DATADIR / "article-001.xml"),
                'XMLFILE': str(DATADIR / "article-001.xml"),
                '--phase': None,
                }
    monkeypatch.setattr(schvalidator.cli,
                        'parsecli',
                        _parsecli)

    result = schvalidator.cli.main()
    assert result == ERROR_CODES[NoISOSchematronFileError]
