#
# Copyright (c) 2017 SUSE Linux GmbH
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

from .exceptions import (NoISOSchematronFileError,
                         OldSchematronError,
                         ProjectFilesNotFoundError,
                         )
from logging import (BASIC_FORMAT,
                     CRITICAL,
                     DEBUG,
                     FATAL,
                     ERROR,
                     INFO,
                     NOTSET,
                     WARN,
                     WARNING,
                     )
from lxml.etree import (QName,
                        SchematronParseError,
                        XMLSyntaxError,
                        XSLTApplyError,
                        XSLTParseError,
                        )


__all__ = ['DEFAULT_LOGGING_DICT',
           'ERROR_CODES',
           'LOGLEVELS', 'LOGNAMES',
           'NSMAP',
           'SCHEMA_TAG',
           ]


# Error codes
# Make an error dictionary that contains both the class and its
# string representation
ERROR_CODES = dict()
for _error, _rc in [(ProjectFilesNotFoundError, 10),
                    (XMLSyntaxError, 20),
                    (XSLTApplyError, 20),
                    (SchematronParseError, 20),
                    (XSLTParseError, 30),
                    (FileNotFoundError, 40),
                    (OSError, 40),
                    (NoISOSchematronFileError, 50),
                    (OldSchematronError, 51),
                    ]:
    ERROR_CODES[_error] = _rc
    ERROR_CODES[repr(_error)] = _rc


#: Prefix to namespace mappings
NSMAP = dict(db="http://docbook.org/ns/docbook",
             # Schematron namespace
             s="http://purl.oclc.org/dsdl/schematron",
             # Obsolete, deprecated namespace of old Schematron
             oldsch="http://www.ascc.net/xml/schematron",
             # Schematron Validation Report namespace
             svrl="http://purl.oclc.org/dsdl/svrl",
             # XML Schema namespace
             xs="http://www.w3.org/2001/XMLSchema",
             )

SCHEMA_TAG = QName(NSMAP['s'], 'schema')
OLD_SCHEMA_TAG = QName(NSMAP['oldsch'], 'schema')


#: Map verbosity to log levels
LOGLEVELS = {None: WARNING,  # 0
             0: WARNING,
             1: INFO,
             2: DEBUG,
             }

#: Map log numbers to log names
LOGNAMES = {NOTSET: 'NOTSET',      # 0
            None: 'NOTSET',
            DEBUG: 'DEBUG',        # 10
            INFO: 'INFO',          # 20
            WARN: 'WARNING',       # 30
            WARNING: 'WARNING',    # 30
            ERROR: 'ERROR',        # 40
            CRITICAL: 'CRITICAL',  # 50
            FATAL: 'CRITICAL',     # 50
            }

#: Dictionary: mapping between ``role`` attribute and log level
ROLEDICT = {None: INFO,  # if no role is set, use INFO
            'warn': WARN,
            'warning': WARN,
            'info': INFO,
            'information': INFO,
            'error': ERROR,
            'fatal': FATAL,
            }

DEBUG_FORMAT = "[%(levelname)s] %(name)s:%(lineno)s %(message)s"
# SIMPLE_FORMAT = "%(levelname)s:%(name)s:%(message)s"


#: Default logging dict for :class:`logging.config.dictConfig`:
DEFAULT_LOGGING_DICT = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'NOTSET',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            # 'stream': 'ext://sys.stderr',
        },
    },
    'loggers': {
        'schvalidator': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        }
    }
}
