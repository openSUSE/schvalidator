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

"""
Validates an XML file with a Schematron schema
"""

from .cli import parsecli
from .cli import __doc__ as clidoc
from .common import ERROR_CODES
from docopt import printable_usage
from .exceptions import ProjectFilesNotFoundError
from .log import log
from .schematron import process
from lxml import etree
import sys


__version__ = "0.1.0"  # flake8: noqa
__author__ = "Thomas Schraitle <toms (AT) suse DOT de>"  # flake8: noqa
__all__ = ('__author__',
           '__version__',
           'main',
           'parsecli',
           'log',
           )  # flake8: noqa


def check_files(args):
    """Checks XML and Schematron files in dictionary

    :param dict args: Dictionary from docopt
    """
    for f, msg in ((args['XMLFILE'], "Need a XML file."),
                   (args['--schema'], "Need a Schematron schema.")):
        if f is None:
            print(clidoc)
            raise ProjectFilesNotFoundError(msg)


def main(cliargs=None):
    """Entry point for the application script

    :param list cliargs: Arguments to parse or None (=use sys.argv)
    :return: return codes from ``ERROR_CODES``
    """

    try:
        args = parsecli(cliargs)
        check_files(args)
        return process(args)

    except (ProjectFilesNotFoundError) as error:
        log.fatal(error)
        return ERROR_CODES.get(repr(type(error)), 255)

    except (etree.XMLSyntaxError,
            etree.XSLTApplyError,
            etree.SchematronParseError) as error:
        log.fatal(error)
        return ERROR_CODES.get(repr(type(error)), 255)

    except etree.XSLTParseError as error:
        log.fatal(error.error_log)
        return ERROR_CODES.get(type(error), 255)

    except (FileNotFoundError, OSError) as error:
        log.fatal(error)
        return ERROR_CODES.get(repr(type(error)), 255)
