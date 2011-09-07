import kinetics.kinematics as kinematics
from kinetics.kinematics import tr
import numpy

import ipdb

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
    self.fg = self.scene.fg
    if hasattr(self,'post_addscene'):
      self.post_addscene()
    # draw object
    self.draw()
    
"""
There should also be strobe, with wrt.
everything under wrt should just continue to progress in time.

Must be PrimitiveCollection
"""
    
    
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
    
  def draw(self):
    pass

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
    dx: trace point x offset in local frame
    dy: trace point y offset in local frame
    dz: trace point z offset in local frame
    
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
      
    if not('wrt' in kwargs):   self.wrt = None
    
    if 'd' in kwargs:
      self.d = Displacement(kwargs['d'])
      del kwargs['d']
    else:
      self.d = Displacement(**kwargs)
    
    self.length = L
    if self.length == -1:
      self.length = 1000
    self.tracepointmatrix = numpy.matrix(numpy.zeros((4,self.length))*numpy.nan) # A ringbuffer matrix containing all tracepoints
    self.tracepointpointer = 0 # A pointer to the active ringbuffer element
    
  def post_addscene(self):
    self.d.addToScene(self.scene,self.frame)
    if not(self.wrt is None):
      self.wrt = self.fg.getFrame(self.wrt)
    
  def update(self,t=None, pre=None):
    self.d.update(t,pre)
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
      return kinematics.inv(wrt)*(self.d.xyz + this*numpy.matrix([[0],[0],[0],[1]]))
    else:
      return self.d.xyz + this * numpy.matrix([[0],[0],[0],[1]])
    
    Primitive.update(self,t,pre)
    
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
  expressions={'x':0,'y':0,'z': 1, 'r': 0.1}

  def __init__(self,**kwargs):
    Primitive.__init__(self,**kwargs)

  def update(self,t=None, pre=None):
    Primitive.update(self,t,pre)
    
    
class Displacement(Primitive):
  """
    dx: x displacement
    dy: y displacement
    dz: z displacement
    
    e: (integer)  frame number 
    
    
    xyz: displacement in world frame coordinates
  """
  expressions={'dx':0,'dy':0,'dz':0}
  
  def __init__(self,*args,**kwargs):
    if len(args)>0 and (args[0],Displacement):
      print "Creating copy"
      orig = args[0]
      self.dx = orig.dx
      self.dy = orig.dy
      self.dz = orig.dz
      self.e = orig.e
      if hasattr(orig,'add'):
        self.add = Displacement(orig.add)
    else:
      if 'e' in kwargs:
        self.e = kwargs['e']
      else:
        self.e = None
    Primitive.__init__(self,**kwargs)
    self.xyz_e = numpy.matrix([[0.0],[0],[0],[0]])

  def update(self,t=None, pre=None):
    if self.e is None:
      print "Skipping"
      self.xyz = numpy.matrix([[0.0],[0],[0],[0]])
      return
    self.xyz_e[0] = self.dx.value()
    self.xyz_e[1] = self.dy.value()
    self.xyz_e[2] = self.dz.value()
    self.xyz = self.e.getFrameMatrix(t) * self.xyz_e
      
    if hasattr(self,'add'):
      self.add.update(t,pre)
      self.xyz += self.add.xyz

  def post_addscene(self):
    if self.e is None:
      self.e = self.frame
    else:
      self.e = self.fg.getFrame(self.e)
    if hasattr(self,'add'):
      self.add.fg = self.fg
      self.add.addToScene(self.scene,self.frame)
    
      
  def __add__(self,d):
    copy = Displacement(self)
  
    if d is self:
      d = Displacement(d)
      
    copy.add = d
    return copy
      
class Vector(Primitive):
  """
    The vector will have it's basepoint in the frame to which it has been assigned (possibly with an extra local T tranformation).
    The vector's head point will be determined by an displacement dx, dy, dz, expressed in a particular frame e.
    
    dx: x displacement
    dy: y displacement
    dz: z displacement

    r: radius
    
    e: (integer)  frame number 
        
    The arrow axis is the z-axis
  """
  
  expressions={'r': 0.1,'x':0,'y':0,'z':0}

  def __init__(self,**kwargs):
    if 'd' in kwargs:
      self.d = Displacement(kwargs['d'])
      del kwargs['d']
    else:
      self.d = Displacement(**kwargs)
      
    print "using", self.d
    Primitive.__init__(self,**kwargs)

  def update(self,t=None, pre=None):
    this = self.frame.getFrameMatrix(t)
    if not(pre is None):
      this = pre*this

    M = self.T.value(t)
    if not(M is None):
      this = this * M
      
    self.d.update(t,pre)
    self.xyz = kinematics.inv(this) * self.d.xyz
    
    Primitive.update(self,t,pre)

  def post_addscene(self):
    self.d.addToScene(self.scene,self.frame)
      
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
    
    
    
    
    
    
    

