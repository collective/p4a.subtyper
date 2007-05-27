import zope.interface
import zope.app.content.interfaces
from p4a.subtyper import interfaces

class IFoo(zope.interface.Interface):
    pass
zope.interface.alsoProvides(IFoo, zope.app.content.interfaces.IContentType)

class DemoDescriptor(object):
    zope.interface.implements(interfaces.IPortalTypedDescriptor)

    title = u'DemoFolderish'
    description = u'Folderish Random Description'
    type_interface = IFoo
    for_portal_type = 'Document'
