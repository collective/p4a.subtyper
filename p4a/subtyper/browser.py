from Acquisition import aq_base
import zope.interface
import zope.component
from p4a.subtyper import interfaces
from p4a.subtyper import utils
import Products.Five.browser
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFDynamicViewFTI import interfaces as IDynamicallyViewableInterface 

class ISubtyperView(zope.interface.Interface):
    def possible_types(): pass
    def has_possible_types(): pass
    def change_type(): pass

class SubtyperView(Products.Five.browser.BrowserView):
    """View for introspecting and possibly changing subtype info for the
    current context.
    """

    zope.interface.implements(ISubtyperView)

    def possible_types(self):
        subtyper = zope.component.getUtility(interfaces.ISubtyper)
        return subtyper.possible_types(self.context)

    def has_possible_types(self):
        return len(self.possible_types()) > 0

    def _redirect(self, msg):
        url = self.context.absolute_url()
        if hasattr(aq_base(self.context), 'getLayout'):
            layout = self.context.getLayout() or ''
            if layout:
                if not url.endswith('/'):
                    url += '/'
                url += layout
        IStatusMessage(self.request).addStatusMessage(msg, type='info')
        self.request.response.redirect(url)
        return ''

    def change_type(self):
        """Change the sub type of the current context.
        """

        subtyper = zope.component.getUtility(interfaces.ISubtyper)

        subtype_name = self.request.get('subtype', None)
        if subtype_name:
            existing = subtyper.existing_type(self.context)
            subtype = subtyper.get_named_type(subtype_name)
            if existing is not None and existing.name == subtype_name:
                selected_layout = False
                dynamic_view = IDynamicallyViewableInterface.IDynamicallyViewable(self.context, None)
                if dynamic_view is not None:
                    if self.context.getLayout() in dynamic_view.getAvailableViewMethods():
                        selected_layout = True
                subtyper.remove_type(self.context)
                msg = 'Removed %s subtype' % subtype.title
                # Check if the default view has disappeared:
                if selected_layout:
                    dynamic_view = IDynamicallyViewableInterface.IDynamicallyViewable(self.context, None)
                    if dynamic_view is None or (self.context.getLayout() in 
                       dynamic_view.getAvailableViewMethods()):
                        if self.context.hasProperty('layout'):
                            self.context.manage_delProperties(['layout'])
            else:
                subtyper.change_type(self.context, subtype_name)
                msg = 'Changed subtype to %s' % subtype.title
        else:
            msg = 'No subtype specified'

        return self._redirect(msg)
