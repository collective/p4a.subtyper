from persistent.dict import PersistentDict

from zope.component import queryUtility
from zope.component import getUtility

from zope.event import notify

import zope.interface
#from zope.interface import directlyProvides
#from zope.interface import directlyProvidedBy
from zope.interface import alsoProvides
from zope.interface import implements

try:
    from zope.annotation import interfaces as annoifaces
except ImportError, err:
    from zope.app.annotation import interfaces as annoifaces

from Products.CMFCore.utils import getToolByName

from p4a.subtyper import interfaces


class SubtypeEvent(object):
    __doc__ = interfaces.ISubtypeEvent
    implements(interfaces.ISubtypeEvent)

    def __init__(self, object, subtype):
        self.object = object
        self.subtype = subtype


class SubtypeAddedEvent(SubtypeEvent):
    __doc__ = interfaces.ISubtypeAddedEvent
    implements(interfaces.ISubtypeAddedEvent)


class SubtypeRemovedEvent(SubtypeEvent):
    __doc__ = interfaces.ISubtypeRemovedEvent
    implements(interfaces.ISubtypeRemovedEvent)


class SubtypeError(Exception):
    pass


class NoSubtypeDefined(SubtypeError):
    pass


class ExistingSubtypeDefined(SubtypeError):
    pass


class DescriptorWithName(object):
    implements(interfaces.IDescriptorWithName)

    def __init__(self, name, descriptor):
        self.name = name
        self.descriptor = descriptor

    def __str__(self):
        return '<DescriptorWithName name=%s; descriptor=%s>' % \
               (self.name, str(self.descriptor))
    __repr__ = __str__


class _DescriptorInfo(object):
    ANNO_KEY = 'p4a.subtyper.DescriptorInfo'

    def __init__(self, context):
        self.context = context
        self.anno = annoifaces.IAnnotations(context, None)

    def _ensure_info(self):
        if self.anno is None:
            annoifaces.IAnnotations(self.context)
        d = self.anno.get(self.ANNO_KEY, None)
        if d is None:
            d = PersistentDict()
            self.anno[self.ANNO_KEY] = d
        return d

    def _set_name(self, v):
        info = self._ensure_info()
        info['descriptor_name'] = v

    def _get_name(self):
        if self.anno is None:
            return None
        d = self.anno.get(self.ANNO_KEY, None)
        if d is None:
            return None
        return d.get('descriptor_name', None)
    name = property(_get_name, _set_name)


class Subtyper(object):
    __doc__ = interfaces.ISubtyper.__doc__
    implements(interfaces.ISubtyper)

    def possible_types(self, obj):
        possible = interfaces.IPossibleDescriptors(obj)
        return (DescriptorWithName(n, c) for n, c in possible.possible)

    def _remove_type(self, obj):
        info = _DescriptorInfo(obj)
        name = info.name
        descriptor = None

        if name is not None:
            info.name = None
            descriptor = queryUtility( \
                interfaces.IContentTypeDescriptor, name=name)
            if descriptor is not None:
                directlyProvides = zope.interface.directlyProvides
                directlyProvidedBy = zope.interface.directlyProvidedBy
                should_have = directlyProvidedBy(obj) - \
                              descriptor.type_interface -\
                              interfaces.ISubtyped
                directlyProvides(obj, should_have)

        return descriptor

    def remove_type(self, obj):
        descriptor = self._remove_type(obj)
        if descriptor is None:
            raise NoSubtypeDefined()
        notify(SubtypeRemovedEvent(obj, descriptor))
        # We want to make sure the old interfaces are cleared from the catalog
        portal_catalog = getToolByName(obj, 'portal_catalog')
        portal_catalog.reindexObject(obj, ['object_provides'])

    def _add_type(self, obj, descriptor_name):
        info = _DescriptorInfo(obj)
        if info.name is not None:
            raise ExistingSubtypeDefined(str(info.name))
        descriptor = getUtility( \
            interfaces.IContentTypeDescriptor, name=descriptor_name)
        info.name = descriptor_name
        alsoProvides(obj, (interfaces.ISubtyped,
                                          descriptor.type_interface, ))
        return descriptor

    def change_type(self, obj, descriptor_name):
        removed = self._remove_type(obj)
        notify(SubtypeRemovedEvent(obj, removed))

        added = self._add_type(obj, descriptor_name)
        notify(SubtypeAddedEvent(obj, added))
        # We want to make sure the new interfaces are present in the catalog
        portal_catalog = getToolByName(obj, 'portal_catalog')
        portal_catalog.reindexObject(obj, ['object_provides'])

    def existing_type(self, obj):
        info = _DescriptorInfo(obj)
        if info.name != None:
            c = queryUtility( \
                interfaces.IContentTypeDescriptor, name=info.name)
            return DescriptorWithName(info.name, c)
        return None

    def get_named_type(self, name):
        return getUtility(interfaces.IContentTypeDescriptor,
                                         name=name)
