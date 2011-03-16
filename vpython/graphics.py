import visual
import visualizer.geometry as geometry

class Primitive(geometry.Primitive):
  def setFrameMatrix(self,M):  # convert T matrix to frame
      self.f.pos=(M[0,3],M[1,3],M[2,3]);
      self.f.axis=(M[0,0],M[1,0],M[2,0]);
      self.f.up=(M[0,1],M[1,1],M[2,1]);

class Box(geometry.Box,Primitive):
  """
    x: length x
    y: length y
    z: length z
  """
  def draw(self):
    self.f = visual.frame()
    self.vis=visual.box(frame=self.f)
    self.draw_update()
    
  def draw_update(self):
    self.vis.length = self.x.value()
    self.vis.height = self.y.value()
    self.vis.width  = self.z.value()
  
  
class Cylinder(geometry.Cylinder,Primitive):
  """
    r: length x
    y: length y
    z: length z
  """
  def draw(self):
    self.f = visual.frame()
    self.vis=visual.cylinder(frame=self.f)
    self.draw_update()
    
  def draw_update(self):
    self.vis.axis = (0,0,self.h.value())
    self.vis.radius = self.r.value()
    
class Scene:
  def __init__(self,scene):
    self.scene=display(x=w, y=0, width=w, height=w, autoscale=True, forward=vector(1,1,-1), newzoom=10,up=(0,0,1))
