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
Validates XML files with Schematron schemas

Usage:
    schvalidator [-h | --help]
    schvalidator [-v ...] [options] SCHEMA XMLFILE

Options:
    -h, --help      Shows this help
    -v              Raise verbosity level
    --version       Prints the version
    --report REPORTFILE
                    save output of Schematron validation to REPORTFILE
    --phase PHASE   a validation phase

Arguments:
    SCHEMA          Path to the Schematron file
    XMLFILE         Path to the XML file to validate
"""


from docopt import docopt
import logging
from logging.config import dictConfig
from lxml import etree

from .common import (DEFAULT_LOGGING_DICT,
                     errorcode, LOGLEVELS,
                     )
from .exceptions import (NoISOSchematronFileError,
                         OldSchematronError,
                         ProjectFilesNotFoundError,
                         )
from .schematron import process

#: Use __package__, not __name__ here to set overall logging level:
log = logging.getLogger(__package__)


def parsecli(cliargs=None):
    """Parse CLI arguments with docopt

    :param list cliargs: List of commandline arguments
    :return: dictionary from docopt
    :rtype: dict
    """
    from schvalidator import __version__
    version = "%s %s" % (__package__, __version__)
    args = docopt(__doc__, argv=cliargs, version=version)
    dictConfig(DEFAULT_LOGGING_DICT)
    log.setLevel(LOGLEVELS.get(args['-v'], logging.DEBUG))

    log.debug("CLI result: %s", args)
    return args


def check_files(args):
    """Checks XML and Schematron files in dictionary

    :param dict args: Dictionary from docopt
    """
    for f, msg in ((args['XMLFILE'], "Need a XML file."),
                   (args['SCHEMA'], "Need a Schematron schema.")):
        if f is None:
            print(__doc__)
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
        return errorcode(error)

    except (etree.XMLSyntaxError,
            etree.XSLTApplyError,
            etree.SchematronParseError) as error:
        log.fatal(error)
        return errorcode(error)

    # except etree.SchematronParseError as error:
    #    log.fatal("Schematron file %r error", args['SCHEMA'])
    #    log.fatal(error)
    #    return errorcode(error)

    except etree.XSLTParseError as error:
        log.fatal(error.error_log)
        return errorcode(error)

    except (FileNotFoundError, OSError) as error:
        log.fatal(error)
        return errorcode(error)

    except (NoISOSchematronFileError, OldSchematronError) as error:
        # print(repr(error))
        log.fatal(error)
        return errorcode(error)
