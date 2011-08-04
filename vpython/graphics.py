import visual
import visualizer.geometry as geometry
import visualizer.colors as colors
import types

class Primitive(geometry.Primitive):
  def setFrameMatrix(self,M):  # convert T matrix to frame
      self.f.pos=(M[0,3],M[1,3],M[2,3]);
      self.f.axis=(M[0,0],M[1,0],M[2,0]);
      self.f.up=(M[0,1],M[1,1],M[2,1]);
      
  def draw(self):
    if hasattr(self,'color'):
      self.vis.color = colors.Color.parse(self.color).getRgbTuple()
      
  def draw_update(self):
    pass
    
class Box(geometry.Box,Primitive):
  """
    x: length x
    y: length y
    z: length z
  """
  def draw(self):
    self.f = visual.frame()
    self.vis=visual.box(frame=self.f)
    Primitive.draw(self)
    self.draw_update()
    
  def draw_update(self):
    self.vis.length = self.x.value()
    self.vis.height = self.y.value()
    self.vis.width  = self.z.value()
    Primitive.draw_update(self)
    
class Arrow(geometry.Arrow,Primitive):
  """
    x: head position x coordinate
    y: head position y coordinate
    z: head position z coordinate
    
    r: radius
        
    The arrow axis is the z-axis
  """
  def draw(self):
    self.f = visual.frame()
    self.vis=visual.arrow(frame=self.f, axis = (0,0,1))
    Primitive.draw(self)
    self.draw_update()
    
  def draw_update(self):
    self.vis.axis = (self.x.value(), self.y.value(), self.z.value())
    self.vis.shaftwidth = self.r.value()
    Primitive.draw_update(self)
  
class Axes(geometry.Axes):
  """
  """
  def __init__(self,**kwargs):
    import visualizer.vpython.graphics as geometryModule
    kwargs.update({'geometryModule': geometryModule})
    geometry.Axes.__init__(self,**kwargs)
    
class Trace(geometry.Trace,Primitive):
  """
    L: length of memory, in number of times that draw_update was called
      -1 means unlimited
  """
  
  
  def draw(self):
    self.f = visual.frame()
    self.vis=visual.curve(frame=self.f, x = [0,1,2])
    Primitive.draw(self)
    self.draw_update()
    
  def draw_update(self):
    if hasattr(self,'curvepoints'):
      self.vis.x = self.curvepoints[0,:]
      self.vis.y = self.curvepoints[1,:]
      self.vis.z = self.curvepoints[2,:]
    Primitive.draw_update(self)
  
class Cylinder(geometry.Cylinder,Primitive):
  """
    r: length x
    y: length y
    z: length z
  """
  def draw(self):
    self.f = visual.frame()
    self.vis=visual.cylinder(frame=self.f)
    Primitive.draw(self)
    self.draw_update()
    
  def draw_update(self):
    self.vis.axis = (0,0,self.h.value())
    self.vis.radius = self.r.value()
    Primitive.draw_update(self)
    
class Scene:
  def __init__(self,scene):
    self.scene=display(x=w, y=0, width=w, height=w, autoscale=True, forward=vector(1,1,-1), newzoom=10,up=(0,0,1))
