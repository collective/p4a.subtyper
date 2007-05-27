import unittest
from zope.testing import doctest
from Testing.ZopeTestCase import FunctionalDocFileSuite
import Products.PloneTestCase.layer

def test_suite():
    flags = doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS
    fsuite = unittest.TestSuite((
        FunctionalDocFileSuite('browser.txt',
                               package='p4a.subtyper.contentmenu',
                               optionflags=flags),
        ))
    fsuite.layer = Products.PloneTestCase.layer.PloneSite

    return fsuite