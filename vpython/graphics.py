import visual
import geometry as geometry

class Primitive(geometry.Primitive):
  def setFrameMatrix(self,M):  # convert T matrix to frame
      self.vis.pos=(M[0,3],M[1,3],M[2,3]);
      self.vis.axis=(M[0,0],M[1,0],M[2,0]);
      self.vis.up=(M[0,1],M[1,1],M[2,1]);

class Box(geometry.Box,Primitive):
  """
    x: length x
    y: length y
    z: length z
  """
  def draw(self):
    self.vis=visual.box(length=self.x.value(0),height=self.y.value(0),width=self.z.value(0))
  

class Scene:
  def __init__(self,scene):
    self.scene=display(x=w, y=0, width=w, height=w, autoscale=True, forward=vector(1,1,-1), newzoom=10,up=(0,0,1))
