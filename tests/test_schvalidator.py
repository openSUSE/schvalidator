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

import docopt
import os.path
import pytest
import sys
from unittest.mock import patch

import schvalidator
from schvalidator.common import ERROR_CODES
from schvalidator.exceptions import ProjectFilesNotFoundError


def test_main(capsys):
    """Checks, if __main__.py can be executed"""
    with pytest.raises(SystemExit):
        path = os.path.dirname(os.path.realpath(__file__)) + "/../src/schvalidator/__main__.py"
        exec(compile(open(path).read(), path, "exec"), {}, {"__name__": "__main__"})


@patch('schvalidator.cli.parsecli')
@patch('schvalidator.cli.check_files')
@pytest.mark.parametrize('schema,xmlfile', [
    (None, "foo.xml"),
    ("schema.sch", ""),
])
def test_main_with_exception(mock_check_files, mock_parsecli,
                             schema, xmlfile):
    mock_check_files.return_value = None
    mock_parsecli.return_value = {'SCHEMA': schema, 'XMLFILE': xmlfile, '--phase': None}
    result = schvalidator.cli.main(["", "schema.sch"])
    #
    assert result == ERROR_CODES[FileNotFoundError]


def test_version(capsys):
    """Checks for correct version"""
    with pytest.raises(SystemExit):
        schvalidator.cli.main(["", "--version"])
    out, _ = capsys.readouterr()
    assert out == "schvalidator {0}\n".format(schvalidator.__version__)


def test_help(capsys):
    """Checks for help output"""
    from schvalidator.cli import __doc__
    with pytest.raises(SystemExit):
        schvalidator.cli.main(["", "--help"])
    out, _ = capsys.readouterr()
    assert out == __doc__.lstrip()


def test_invalid():
    """Checks for invalid option"""
    with pytest.raises(docopt.DocoptExit):
        schvalidator.cli.main(["", "--asdf"])
