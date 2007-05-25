import zope.interface
import zope.app.content.interfaces
from p4a.subtyper import interfaces

class SubtypeEvent(object):
    __doc__ = interfaces.ISubtypeEvent
    zope.interface.implements(interfaces.ISubtypeEvent)

    def __init__(self, object, subtype):
        self.object = object
        self.subtype = subtype

class SubtypeAddedEvent(SubtypeEvent):
    __doc__ = interfaces.ISubtypeAddedEvent
    zope.interface.implements(interfaces.ISubtypeAddedEvent)

class SubtypeRemovedEvent(SubtypeEvent):
    __doc__ = interfaces.ISubtypeRemovedEvent
    zope.interface.implements(interfaces.ISubtypeRemovedEvent)

class NoSubtypeDefined(Exception): pass

class Subtyper(object):
    __doc__ = interfaces.ISubtyper.__doc__
    zope.interface.implements(interfaces.ISubtyper)

    def possible_types(self, obj):
        return (x.type_interface for x in self.possible_descriptors(obj))

    def possible_descriptors(self, obj):
        possible = interfaces.IPossibleTypes(obj)
        return possible.possible

    def _remove_type(self, obj):
        type_ = self.existing_type(obj)

        if type_ is not None:
            directlyProvides = zope.interface.directlyProvides
            directlyProvidedBy = zope.interface.directlyProvidedBy
            directlyProvides(obj, directlyProvidedBy(obj) - type_)

        return type_

    def remove_type(self, obj):
        type_ = self._remove_type(obj)
        if type_ is None:
            raise NoSubtypeDefined()
        zope.event.notify(SubtypeRemovedEvent(obj, type_))

    def _add_type(self, obj, type_):
        zope.interface.alsoProvides(obj, (type_,))

    def change_type(self, obj, type_):
        removed = self._remove_type(obj)
        zope.event.notify(SubtypeRemovedEvent(obj, removed))

        self._add_type(obj, type_)
        zope.event.notify(SubtypeRemovedEvent(obj, type_))

    def existing_type(self, obj):
        type_ = None
        for x in zope.interface.directlyProvidedBy(obj):
            if zope.app.content.interfaces.IContentType.providedBy(x):
                type_ = x
                break
        return type_
