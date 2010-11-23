import types
import fdl.graph
from numpy import eye

class Frame(fdl.graph.Frame):
  def __init__(self,base,matrix,name='',description='',id=None):
    fdl.graph.Frame.__init__(self,base,base.fg.expressionManager.createExpression(matrix,force=1),name,description,id)
    
  def getFrameMatrix(self,t=None):
    if isinstance(self,fdl.graph.WorldFrame):
      return self.fg.eye
    if isinstance(self.base,fdl.graph.WorldFrame):
      return self.matrix.value(t)
    return self.base.getFrameMatrix(t) * self.matrix.value(t)
    
class WorldFrame(fdl.graph.WorldFrame):
  def getFrameMatrix(self,t=None):
    return self.fg.eye

class FrameGraph(fdl.graph.FrameGraph):
  eye = eye(4)
  def __init__(self,expressionManager=None):
    fdl.graph.FrameGraph.__init__(self)
    self.expressionManager = expressionManager

