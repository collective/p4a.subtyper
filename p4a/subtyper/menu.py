import logging
import zope.component
import zope.interface
from zope.app.publisher.interfaces.browser import IBrowserMenu
from zope.app.publisher.browser.menu import BrowserMenu
from zope.app.component.interface import interfaceToName
from p4a.subtyper import interfaces
from p4a.subtyper import utils

logger = logging.getLogger('p4a.subtyper.menu')

class SubtypesMenu(BrowserMenu):
    """A menu with items representing all possible subtypes for the current
    context.
    """

    zope.interface.implements(IBrowserMenu)

    def _get_menus(self, object, request): 
        subtyper = zope.component.getUtility(interfaces.ISubtyper)
        existing = subtyper.existing_type(object)

        result = []
        for subtype in subtyper.possible_types(object):
            descriptor = subtype.descriptor

            d = {'title': descriptor.title,
                 'description': descriptor.description or u'',
                 'action': '%s/@@subtyper/change_type?descriptor=%s' % \
                     (object.absolute_url(),
                      utils.dotted_name(descriptor.__class__)),
                 'selected': descriptor.type_interface == existing,
                 'icon': '',
                 'extra': None,
                 'submenu': None,
                 'subtype': subtype }
            result.append(d)

        return result

    def getMenuItems(self, object, request):
        try:
            return self._get_menus(object, request)
        except Exception, e:
            # it can be very difficult to troubleshoot errors here
            # because sometimes it bubbles up as AttributeError's which
            # the zope2 publisher handles in a very bizarre manner

            logger.exception(e)
            raise
