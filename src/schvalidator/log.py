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
Logging setup
"""

import logging
import sys

__all__ = ('log', 'role2level', 'schlog',
           'setloglevel', 'LOGLEVELS', 'ROLEDICT')

#: ``log`` is the object to use for all log events
log = logging.getLogger(__file__)
_ch = logging.StreamHandler(sys.stderr)
_frmt = logging.Formatter('[%(levelname)s]: '
                          '%(message)s', '%H:%M:%S')
_ch.setFormatter(_frmt)
log.setLevel(logging.DEBUG)
log.addHandler(_ch)

#: ``schlog`` is the logger for all Schematron related output
schlog = logging.getLogger('schematron')
_ch = logging.StreamHandler(sys.stderr)
_frmt = logging.Formatter('[%(levelname)s]: %(message)s')
_ch.setFormatter(_frmt)
schlog.setLevel(logging.INFO)
schlog.addHandler(_ch)

#: Dictionary: Log levels to map verbosity level to logging values
LOGLEVELS = {None: logging.NOTSET,  # 0
             0: logging.NOTSET,     # 0
             1: logging.INFO,       # 20
             2: logging.DEBUG,      # 10
             }
#: Dictionary: mapping between ``role`` attribute and log level
ROLEDICT = {None: logging.INFO,  # if no role is set, use INFO
            'warn': logging.WARN,
            'warning': logging.WARN,
            'info': logging.INFO,
            'information': logging.INFO,
            'error': logging.ERROR,
            'fatal': logging.FATAL,
            }


def setloglevel(verbose):
    """Set log level according to verbose argument

    :param int verbose: verbose level to set
    """
    log.setLevel(LOGLEVELS.get(verbose, logging.DEBUG))


def role2level(rolelevel):
    """Return the log level

    :param str rolelevel: The value of the ``role`` attribute
    """
    return ROLEDICT.get(rolelevel)
