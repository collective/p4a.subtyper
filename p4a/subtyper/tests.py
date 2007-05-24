import unittest
from zope.testing import doctest
from zope.component import testing

def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS
    return unittest.TestSuite((
        doctest.DocFileSuite('subtyping.txt',
                             setUp=testing.setUp,
                             tearDown=testing.tearDown,
                             optionflags=flags),
        ))
