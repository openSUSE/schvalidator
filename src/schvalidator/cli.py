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
    schvalidator [-v ...] [options] --schema SCHEMA XMLFILE

Options:
    -h, --help      Shows this help
    -v              Raise verbosity level
    --version       Prints the version
    --report REPORTFILE
                    save output of Schematron validation to REPORTFILE
    --phase PHASE   a validation phase
    --schema SCHEMA
                    Points to the Schematron file
    XMLFILE         Path to the XML file to validate
"""


from docopt import docopt
# from docopt import printable_usage
from lxml import etree

from .common import ERROR_CODES
from .exceptions import ProjectFilesNotFoundError
from .log import log, setloglevel
from .schematron import process


def parsecli(cliargs=None):
    """Parse CLI arguments with docopt

    :param list cliargs: List of commandline arguments
    :return: dictionary from docopt
    :rtype: dict
    """
    from schvalidator import __version__
    version = "%s %s" % (__package__, __version__)
    args = docopt(__doc__, argv=cliargs, version=version)
    # verbose = args['-v'] if args['-v'] else None
    setloglevel(args['-v'])
    log.debug("Got the following options and arguments: %s", args)
    return args


def check_files(args):
    """Checks XML and Schematron files in dictionary

    :param dict args: Dictionary from docopt
    """
    for f, msg in ((args['XMLFILE'], "Need a XML file."),
                   (args['--schema'], "Need a Schematron schema.")):
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
        return ERROR_CODES.get(repr(type(error)), 255)

    except (etree.XMLSyntaxError,
            etree.XSLTApplyError,
            etree.SchematronParseError) as error:
        log.fatal(error)
        return ERROR_CODES.get(repr(type(error)), 255)

    # except etree.SchematronParseError as error:
    #    log.fatal("Schematron file %r error", args['--schema'])
    #    log.fatal(error)
    #    return ERROR_CODES.get(repr(type(error)), 255)

    except etree.XSLTParseError as error:
        log.fatal(error.error_log)
        return ERROR_CODES.get(type(error), 255)

    except (FileNotFoundError, OSError) as error:
        log.fatal(error)
        return ERROR_CODES.get(repr(type(error)), 255)
