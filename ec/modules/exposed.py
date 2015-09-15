r"""
exposed
=======

A module for members that are used by ec, as well as exposed to the scripts.

"""
def static(cls):
  r"""Converts the given class into a static one, by changing all the methods of it into static methods.

  Args:
    cls (class): The class to be converted.
  """
  for attr in dir(cls):
      im_func = getattr(getattr(cls, attr), 'im_func', None)
      if im_func:
        setattr(cls, attr, staticmethod(im_func))

  return cls
