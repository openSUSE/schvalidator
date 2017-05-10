
import pytest
from schvalidator.common import ERROR_CODES
import schvalidator.schematron as schematron
from schvalidator.exceptions import ProjectFilesNotFoundError


def test_filenotfound1():
    #
    args = {'SCHEMA': 'schema-does-not-exist.sch',
            '--phase': None,
            'XMLFILE': 'file-does-not-exist.xml'}

    with pytest.raises((FileNotFoundError, OSError)):
        schematron.process(args)


def test_filenotfound2():
    #
    from schvalidator.cli import main

    result = main(['schema-does-not-exist.sch',
              'file-does-not-exist.xml'])
    assert result == ERROR_CODES[FileNotFoundError]
