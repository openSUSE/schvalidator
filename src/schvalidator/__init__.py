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
schvalidator Module
===================

.. default-domain:: py

Validates an XML file with a Schematron schema
"""

import logging


__version__ = "0.2.0"  # flake8: noqa
__author__ = "Thomas Schraitle"  # flake8: noqa
__proc__ = "schvalidator"
__url__ = "https://github.com/openSUSE/schvalidator"
__email__ = "tom_schr (AT) suse DOT de"
__summary__ = __doc__


#: Set default logging handler to avoid "No handler found" warnings.
# See https://docs.python.org/3/howto/logging.html#library-config
logging.getLogger().addHandler(logging.NullHandler())
