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

from .exceptions import ProjectFilesNotFoundError
from lxml.etree import (SchematronParseError,
                        XMLSyntaxError,
                        XSLTApplyError,
                        XSLTParseError,
                        )


__all__ = ['ERROR_CODES']


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
                    ]:
    ERROR_CODES[_error] = _rc
    ERROR_CODES[repr(_error)] = _rc
