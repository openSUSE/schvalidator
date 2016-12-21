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
    schvalidator [-vvv | -vv | -v] [options] --schema SCHEMA XMLFILE

Options:
    -h, --help      Shows this help
    -v, -vv, -vv    Raise verbosity level
    --version       Prints the version
    --report REPORTFILE
                    save output of Schematron validation to REPORTFILE
    --phase PHASE   a validation phase
    --schema SCHEMA
                    Points to the Schematron file
    XMLFILE         Path to the XML file to validate
"""


from docopt import docopt

from .log import log, setloglevel


def parsecli(cliargs=None):
    """Parse CLI arguments with docopt
    """
    from schvalidator import __version__
    version = "%s %s" % (__package__, __version__)
    args = docopt(__doc__, argv=cliargs, version=version)
    # verbose = args['-v'] if args['-v'] else None
    verbose = args['-v']
    setloglevel(verbose)
    log.debug("Got the following options and arguments: %s", args)
    return args
