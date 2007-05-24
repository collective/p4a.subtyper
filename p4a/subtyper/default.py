import Acquisition
import zope.interface
import zope.component
from p4a.subtyper import interfaces
import Products.Archetypes.interfaces

class PossibleDescriptors(object):
    zope.interface.implements(interfaces.IPossibleDescriptors)

    def __init__(self, possible=[], comment=None):
        self._possible = possible
        self._comment = comment

    @property
    def possible(self):
        return self._possible

    def __str__(self):
        return '<PossibleDescriptors comment=%s>' % (self._comment or '')
    __repr__ = __str__

@zope.component.adapter(Products.Archetypes.interfaces.IBaseFolder)
@zope.interface.implementer(interfaces.IPossibleDescriptors)
def folderish_possible_descriptors(context):
    portal_type = getattr(Acquisition.aq_inner(context), 'portal_type', None)
    if portal_type is None:
        return PossibleDescriptors()

    possible = zope.component.getAllUtilitiesRegisteredFor \
               (interfaces.IPortalTypedFolderishDescriptor)
    return PossibleDescriptors([c for c in possible
                                if c.for_portal_type == portal_type],
                               'folderish')

@zope.component.adapter(Products.Archetypes.interfaces.IBaseContent)
@zope.interface.implementer(interfaces.IPossibleDescriptors)
def nonfolderish_possible_descriptors(context):
    portal_type = getattr(Acquisition.aq_inner(context), 'portal_type', None)
    if portal_type is None:
        return PossibleDescriptors()

    all = zope.component.getAllUtilitiesRegisteredFor \
          (interfaces.IPortalTypedDescriptor)
    folderish = zope.component.getAllUtilitiesRegisteredFor \
          (interfaces.IPortalTypedFolderishDescriptor)

    all = set([c for c in all if c.for_portal_type == portal_type])
    folderish = set([c for c in folderish
                     if c.for_portal_type == portal_type])

    return PossibleDescriptors(list(all.difference(folderish)),
                               'nonfolderish')
