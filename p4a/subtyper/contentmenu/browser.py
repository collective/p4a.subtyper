from Products.Five.browser import BrowserView
import Globals
import AccessControl.SecurityInfo


class ContentMenuView(BrowserView):
    """A view for the content menu.
    """

    security = AccessControl.SecurityInfo.ClassSecurityInfo()

    security.declarePublic('macros')

    @property
    def macros(self):
        return self.index.macros

Globals.InitializeClass(ContentMenuView)


class TestView(BrowserView):
    """Simple replacement of the standard zope2 test function.
    """

    def test(self, condition, trueval, falseval):
        if condition:
            return trueval
        return falseval

    def __call__(self, condition, trueval, falseval):
        return self.test(condition, trueval, falseval)
