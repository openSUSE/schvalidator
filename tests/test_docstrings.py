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


import inspect
import pytest
import re
import schvalidator


def getallfunctions(module=schvalidator):
    def getfunctions(_module):
        for _, func, in inspect.getmembers(_module,
                                              inspect.isfunction):
            if func.__module__ == _module.__name__:
                yield func
    def getmodules(_module):
        for _, m, in inspect.getmembers(_module,
                                              inspect.ismodule):
            if m.__package__ == _module.__package__:
                yield m

    # allfunctions = []
    for ff in getfunctions(module):
         yield ff
    for mm in getmodules(module):
        for ff in getfunctions(mm):
            yield ff

modfuncs = list(getallfunctions(schvalidator))
modfuncsnames = [ff.__name__ for ff in modfuncs]


@pytest.mark.parametrize("func",
                         modfuncs,
                         ids=modfuncsnames
                         )
def test_docstrings_nonempty(func):
    fname = func.__name__
    doc = func.__doc__
    assert doc is not None, "Need an non-empty docstring for %r" % fname


@pytest.mark.parametrize("func",
                         modfuncs,
                         ids=modfuncsnames
                         )
def test_docstrings_args(func):
    fname = func.__name__
    doc = func.__doc__
    assert doc is not None
    if func.__code__.co_argcount:
        for arg in inspect.getargspec(func).args:
            m = re.search(":param\s+\w*\s*%s:" % arg, doc)
            assert m, "Func argument %r " \
                "not explained in docstring " \
                "of function %r" % (arg, fname)
