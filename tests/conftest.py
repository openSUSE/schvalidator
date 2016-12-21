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

import pytest
import py

# TESTDIR = py.path.local(__file__).dirpath()
DATADIR = py.path.local(__file__).parts()[-2] / "data"


def pytest_generate_tests(metafunc):
    """Replace the schtestcases fixture by all *.{xml,sch,svrl}
    files in tests. A testcase contains the following set of files:

    * :file:`*-001.xml` (required)::
      the XML file to test
    * :file:`-001.sch` (required)::
      the corresponding Schematron schema for the previous test
    * :file:`-001.svrl` (optional)::
      a XML file of the XML report. The XML file contains the root element
      ``svrl:schematron-output``. This is only needed, to compare it if
      the results are too difficult to test.
    """
    if 'schtestcase' in metafunc.fixturenames:
        testcases = []
        allxmltests = DATADIR.listdir('*.xml')
        for test in allxmltests:
            base, number = test.purebasename.split("-")
            try:
                schematron = DATADIR.listdir("*-%s.sch" % number)[0]
            except IndexError:
                pytest.fail("XML file %r with no "
                            "corresponding Schematron file." % test.purebasename)
            try:
                svrl = DATADIR.listdir("*-%s.svrl" % number)[0]
            except IndexError:
                pytest.fail("XML file %r with no corresponding "
                            "report file." %
                            test.purebasename)
            testcases.append((test, schematron, svrl))

        # Generates the pure file names for pytest to identify the test better
        # See http://docs.pytest.org/en/latest/parametrize.html#_pytest.python.Metafunc.parametrize
        ids = [f.purebasename for f in allxmltests]
        metafunc.parametrize("schtestcase", testcases, ids=ids)
