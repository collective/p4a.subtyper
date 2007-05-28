import zope.component
import zope.interface
from zope.app.publisher.interfaces.browser import IBrowserMenu
from zope.app.publisher.browser.menu import BrowserMenu
from zope.app.component.interface import interfaceToName
from p4a.subtyper import interfaces
from p4a.subtyper import utils

class SubtypesMenu(BrowserMenu):
    """A menu with items representing all possible subtypes for the current
    context.
    """

    zope.interface.implements(IBrowserMenu)

    def getMenuItems(self, object, request):
        subtyper = zope.component.getUtility(interfaces.ISubtyper)
        existing = subtyper.existing_type(object)

        result = []
        for subtype in subtyper.possible_types(object):
            d = {'title': subtype.title,
                 'description': subtype.description or u'',
                 'action': '%s/@@subtyper/change_type?descriptor=%s' % \
                     (object.absolute_url(),
                      utils.dotted_name(subtype.__class__)),
                 'selected': subtype.type_interface == existing,
                 'icon': '',
                 'extra': None,
                 'submenu': None,
                 'subtype': subtype }
            result.append(d)

        return result
