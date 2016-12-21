
import pytest
import schvalidator.schematron as schematron
from schvalidator.exceptions import ProjectFilesNotFoundError


def test_filenotfound1():
    #
    args = {'--schema': 'schema-does-not-exist.sch',
            '--phase': None,
            'XMLFILE': 'file-does-not-exist.xml'}

    with pytest.raises((FileNotFoundError, OSError)):
        schematron.process(args)


def test_filenotfound2():
    #
    from schvalidator import main

    with pytest.raises(SystemExit):
        main(['--schema', 'schema-does-not-exist.sch',
              'file-does-not-exist.xml'])
