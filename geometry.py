import kinetics.kinematics as kinematics
from kinetics.kinematics import tr
import numpy

class KeywordAttributes:
  def __init__(self,**kwargs):
    for k,v in kwargs.items():
      setattr(self,k,v)

class Visualizer:
  scene=None
  def addToScene(self,scene,frame):
    self.scene=scene
    # Promote all expression attributes to expressions
    for k,v in self.expressions.items():
      if not(hasattr(self,k)):
        setattr(self,k,v)
      else:
        v = getattr(self,k)
      setattr(self,k,self.scene.expressionManager.createExpression(v))
    # associate object with frame
    self.frame = self.scene.fg.getFrame(frame)
    # draw object
    self.draw()
    
class PrimitiveCollection(KeywordAttributes,Visualizer):
  """
  
  Keywords:
   T  a transformation on this object
   e.g.   T = 'tr(x,y,z)'
   
   s scale
     1 == normal
     >1 big
     <1 small
  
  """
  expressions = {'T' : None, 's': 1 }
  
  inherit = ['color']

  def __init__(self,**kwargs):
    self.expressions.update(PrimitiveCollection.expressions)
    self.objects = []
    KeywordAttributes.__init__(self,**kwargs)
    if not(hasattr(self,'geometryModule')):
      import visualizer.geometry as geometryModule
      self.geometryModule = geometryModule
  
  def addToScene(self,scene,frame):
    Visualizer.addToScene(self,scene,frame)
    for o in self.objects:
      o.addToScene(scene,0) # Add to world frame
    
  def add(self,obj):
    """
    Add an object or a list of objects
    """
    if not(isinstance(obj,list)):
      obj = [obj]
    

    for inherited in self.inherit:
      if hasattr(self,inherited):
        for o in obj:
          if not(hasattr(o,inherited)):
            setattr(o,inherited,getattr(self,inherited))

    self.objects+=obj
  
  def update(self,t=None, pre=None):
    M = self.T.value(t)
    mtx = pre
    if mtx is None:
      mtx = self.frame.getFrameMatrix(t)
    if not(M is None):
      mtx = mtx*M
    for o in self.objects:
      o.update(t, pre=mtx)
      
  def draw(self,*arg,**kwargs):
    pass

class Primitive(KeywordAttributes,Visualizer):
  """
  
  Keywords:
   T  a transformation on this object
   e.g.   T = 'tr(x,y,z)'
  
   s scale
     1 == normal
     >1 big
     <1 small
  
  """
  expressions = {'T' : None, 's': 1}
  
  def __init__(self,**kwargs):
    self.expressions.update(Primitive.expressions)
    KeywordAttributes.__init__(self,**kwargs)
  pass
  
  def update(self,t=None, pre=None):
    M = self.T.value(t)
    mtx = pre
    if mtx is None:
      mtx = self.frame.getFrameMatrix(t)
    else:
      mtx = pre*self.frame.getFrameMatrix(t)
    if M is None:
      self.setFrameMatrix(mtx)
    else:
      self.setFrameMatrix(mtx*M)
    self.draw_update()

class Box(Primitive):
  """
    x: length x
    y: length y
    z: length z
  """
  expressions = {'x':1,'y':1,'z':1}

  def __init__(self,**kwargs):
    Primitive.__init__(self,**kwargs)
    
class Trace(Primitive):
  """
    x: trace point x coordinate
    y: trace point y coordinate
    z: trace point z coordinate
    
    L (optional, default -1): length of memory, in number of times that draw_update was called
      -1 means unlimited
      
    wrt (optional, default world): a Frame with respect to which the trace must be taken.
    
    
  """
  expressions = {'x':0,'y':0,'z':0}

  def __init__(self,**kwargs):
    Primitive.__init__(self,**kwargs)
    
    if 'L' in kwargs:
      L = kwargs['L']
    else:
      L = -1
      
    if not('wrt' in kwargs):  self.wrt = None
    
    self.length = L
    if self.length == -1:
      self.length = 1000
    self.tracepointmatrix = numpy.matrix(numpy.zeros((4,self.length))*numpy.nan) # A ringbuffer matrix containing all tracepoints
    self.tracepointpointer = 0 # A pointer to the active ringbuffer element
    
  def update(self,t=None, pre=None):

    self.tracepointmatrix[:,self.tracepointpointer] = self.getTracePoint(t,pre)

    #print "origmatrix = ", self.tracepointmatrix

    if not(self.wrt is None):
      this = self.frame.getFrameMatrix(t)
      wrt = self.wrt.getFrameMatrix(t)
      prod = kinematics.inv(this) * wrt * self.tracepointmatrix
    else:
      this = self.frame.getFrameMatrix(t)
      prod =  kinematics.inv(this) * self.tracepointmatrix
    
    
    self.curvepoints = numpy.hstack((prod[:3,self.tracepointpointer+1:],prod[:3,:self.tracepointpointer+1]))
    self.curvepoints = numpy.array(self.curvepoints)
    
    self.tracepointpointer = (self.tracepointpointer + 1) % self.length
    Primitive.update(self,t,pre)
    
  def getTracePoint(self,t,pre):
    """
    Get a 4-element vector which is the point that must be stored and shown with respect to wrt
    """
    this = self.frame.getFrameMatrix(t)
    if not(pre is None):
      this = pre*this

    M = self.T.value(t)
    if not(M is None):
      this = this * M
    
    if not(self.wrt is None):
      wrt = self.wrt.getFrameMatrix(t)
      return (kinematics.inv(wrt)*this*numpy.matrix([[self.x.value(t)],[self.y.value(t)],[self.z.value(t)],[1]]))
    else:
      return (this*numpy.matrix([[self.x.value(t)],[self.y.value(t)],[self.z.value(t)],[1]]))
    
class Cylinder(Primitive):
  """
    r: radius
    h: height
    
    The cylinder axis is the z-axis
  """
  expressions={'r':1,'h':0.1}

  def __init__(self,**kwargs):
    Primitive.__init__(self,**kwargs)

  def update(self,t=None, pre=None):
    Primitive.update(self,t,pre)
    self.radius = self.r.value(t)
    self.height = self.h.value(t)
    
class Text(Primitive):
  """
    caption = 
    
  """
  expressions={'caption': 'foo'}

  def __init__(self,**kwargs):
    Primitive.__init__(self,**kwargs)

  def update(self,t=None, pre=None):
    Primitive.update(self,t,pre)
    
    
class Arrow(Primitive):
  """
    x: head position x coordinate
    y: head position y coordinate
    z: head position z coordinate
    
    r: radius
        
    The arrow axis is the z-axis
  """
  expressions={'x':0,'y':0,'z': 0, 'r': 0.1}

  def __init__(self,**kwargs):
    Primitive.__init__(self,**kwargs)

  def update(self,t=None, pre=None):
    Primitive.update(self,t,pre)
    
    
class Axes(PrimitiveCollection):
  """
  """
  def __init__(self,**kwargs):
    PrimitiveCollection.__init__(self,**kwargs)
    self.add([self.geometryModule.Arrow(x=1,y=0,z=0),
              self.geometryModule.Arrow(x=0,y=1,z=0),
              self.geometryModule.Arrow(x=0,y=0,z=1),
              self.geometryModule.Text(caption="'x'",T=tr(1,0,0)),
              self.geometryModule.Text(caption="'y'",T=tr(0,1,0)),
              self.geometryModule.Text(caption="'z'",T=tr(0,0,1))
              ])
    
    
    
    
    
    
    

