import zope.interface

class IContentTypeDescriptor(zope.interface.Interface):
    title = zope.schema.TextLine(title=u'Title')
    description = zope.schema.Text(title=u'Description')
    type_interface = zope.schema.InterfaceField(title=u'Type Interface')

class IFolderishContentTypeDescriptor(IContentTypeDescriptor):
    allowed_child_portal_types = zope.schema.Set( \
        title=u'Allowed Child Portal Types'
        )

class _IPortalTyped(IContentTypeDescriptor):
    for_portal_type = zope.schema.TextLine(title=u'For Portal Type')

class IPortalTypedDescriptor(IContentTypeDescriptor,
                             _IPortalTyped):
    pass

class IPortalTypedFolderishDescriptor(IFolderishContentTypeDescriptor,
                                      _IPortalTyped):
    pass

class IPossibleDescriptors(zope.interface.Interface):
    possible = zope.schema.List( \
        title=u'Possible',
        value_type=zope.schema.Object(title=u'Possible',
                                      schema=IContentTypeDescriptor)
        )
