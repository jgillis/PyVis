

class KeywordAttributes:
  def __init__(self,**kwargs):
    for k,v in kwargs.items():
      setattr(self,k,v)

class Visualizer:
  scene=None
  def addToScene(self,scene,frame):
    print self
    self.scene=scene
    # Promote all expression attributes to expressions
    for k,v in self.expressions.items():
      if not(hasattr(self,k)):
        setattr(self,k,v)
      setattr(self,k,self.scene.expressionManager.createExpression(getattr(self,k)))
    # associate object with frame
    self.frame = self.scene.fg.getFrame(frame)
    # draw object
    self.draw()
    
class PrimitiveCollection(KeywordAttributes,Visualizer):
  pass


class Primitive(KeywordAttributes,Visualizer):
  def __init__(self,**kwargs):
    KeywordAttributes.__init__(self,**kwargs)
  pass
  
  def update(self,t=None):
    self.setFrameMatrix(self.frame.getFrameMatrix(t))
    self.draw_update()

class Box(Primitive):
  """
    x: length x
    y: length y
    z: length z
  """
  expressions={'x':1,'y':1,'z':1}

  def __init__(self,**kwargs):
    Primitive.__init__(self,**kwargs)
  
class Cylinder(Primitive):
  """
    r: radius
    h: height
    
    The cylinder axis is the z-axis
  """
  expressions={'r':1,'h':0.1}

  def __init__(self,**kwargs):
    Primitive.__init__(self,**kwargs)

  def update(self,t=None):
    Primitive.update(self,t)
    self.radius = self.r.value()
    self.height = self.h.value()
    
