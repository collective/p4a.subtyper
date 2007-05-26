import urllib
import zope.interface
import zope.component
from p4a.subtyper import interfaces
from p4a.subtyper import utils
import Products.Five.browser

class ISubtyperView(zope.interface.Interface):
    def possible_descriptors(): pass 
    def has_possible_descriptors(): pass
    def change_type(): pass

class SubtyperView(Products.Five.browser.BrowserView):
    """View for introspecting and possibly changing subtype info for the
    current context.
    """

    zope.interface.implements(ISubtyperView)

    def possible_descriptors(self):
        subtyper = zope.component.getUtility(interfaces.ISubtyper)
        return subtyper.possible_descriptors(self.context)

    def has_possible_descriptors(self):
        return len(self.possible_descriptors()) > 0

    def _redirect(self, msg):
        url = self.context.absolute_url()
        self.request.response.redirect(url + '?portal_status_message=' + \
                                       urllib.quote(msg))
        return ''

    def change_type(self):
        """Change the sub type of the current context.
        """

        subtyper = zope.component.getUtility(interfaces.ISubtyper)

        descriptor_name = self.request.get('descriptor', None)
        if descriptor_name:
            descriptor = utils.name_to_class(descriptor_name)()
            msg = 'Changed subtype to %s' % descriptor.title
            subtyper.change_type(self.context, descriptor.type_interface)
        else:
            msg = 'No subtype specified'

        return self._redirect(msg)
