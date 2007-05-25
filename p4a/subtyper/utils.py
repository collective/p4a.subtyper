
_marker = object()

def adapt_docs(src, tgt):
    """Ensure the target object has the same __doc__ on itself and any
    callable attributes it might have that the equivalent in the source
    object has.

      >>> class Foo(object):
      ...     'this is foo'
      ...     def func1(self):
      ...         'this is func1'
      ...     def func2(self): pass
      ...     def func3(self):
      ...         'this is func3'
      ...     randattr = 'abc'

      >>> class Bar(object):
      ...    def func1(self): pass
      ...    def func2(self): pass

      >>> adapt_docs(Foo, Bar)

      >>> Bar.__doc__
      'this is foo'
      >>> Bar.func1.__doc__
      'this is func1'
      >>> Bar.func2.__doc__
      None
    """

    tgt.__doc__ = src.__doc__

    for key, value in src.__dict__.items():
        if callable(value):
            attr = getattr(tgt, key, _marker)
            if attr != _marker and callable(attr):
                attr.__doc__ = value.__doc__
