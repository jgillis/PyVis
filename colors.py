import types

class Color(object):
  rgb = (0,0,0)
  @staticmethod
  def parse(obj):
    if isinstance(obj,Color):
      return obj.__class__
    if isinstance(obj,type) and issubclass(obj,Color):
      return obj
    if isinstance(obj,types.StringType):
      sc = Color.__subclasses__()
      for c in sc:
        if c.__name__ == obj:
          return c
    if isinstance(obj, tuple):
      return custom(obj)
          
    raise Exception("Unknown color: %s" % (str(obj)))

  @classmethod
  def getRgbTuple(cls):
    return cls.rgb
  
class custom(Color):
  def __init__(self,rgbtuple):
    self.rgbtuple = rgbtuple
    
  def getRgbTuple(self):
    return self.rgbtuple
  
class red(Color):
  rgb = (1,0,0)
  
class green(Color):
  rgb = (0,1,0)
  
class blue(Color):
  rgb = (0,0,1)
  
class white(Color):
  rgb = (1,1,1)

class black(Color):
  rgb = (0,0,0)
  
class yellow(Color):
  rgb = (1,1,0)
