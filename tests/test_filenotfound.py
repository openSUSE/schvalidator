
import pytest
import os.path
from schvalidator.schematron import check_args, process
from schvalidator.exceptions import ProjectFilesNotFoundError


@pytest.mark.parametrize('schema,xmlfile', [
    (None, 'file-does-not-exist.xml'),
    ('schema-does-not-exist.sch', None),
])
def test_check_args(monkeypatch, schema, xmlfile):
    args = {'--schema': schema,
            'XMLFILE': xmlfile}
    def mockreturn(filename):
        return filename is None

    monkeypatch.setattr(os.path,
                        'exists',
                        mockreturn)
    with pytest.raises(ProjectFilesNotFoundError):
        check_args(args)


def test_filenotfound1():
    #
    args = {'--schema': 'schema-does-not-exist.sch',
            'XMLFILE': 'file-does-not-exist.xml'}

    with pytest.raises((FileNotFoundError, OSError)):
        process(args)


def test_filenotfound2():
    #
    from schvalidator import main

    with pytest.raises(SystemExit):
        main(['--schema', 'schema-does-not-exist.sch',
              'file-does-not-exist.xml'])
