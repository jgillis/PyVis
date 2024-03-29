import types
import fdl.graph
from numpy import eye

class Frame(fdl.graph.Frame):
  """
  We inherit from fdl.graph.Frame to have additional semantics: base, name, matrix, description
  """
  def __init__(self,base,matrix,name='',description='',id=None):
    fdl.graph.Frame.__init__(self,base,base.fg.expressionManager.createExpression(matrix,force=1),name,description,id)
    
    
  # Caching might be good here
  def getFrameMatrix(self,t=None):
    if isinstance(self,fdl.graph.WorldFrame):
      return self.fg.eye
    if isinstance(self.base,fdl.graph.WorldFrame):
      return self.matrix.value(t)
    return self.base.getFrameMatrix(t) * self.matrix.value(t)
    
class WorldFrame(fdl.graph.WorldFrame):
  """
  A class that represents the world Frame
  """
  def getFrameMatrix(self,t=None):
    return self.fg.eye

class FrameGraph(fdl.graph.FrameGraph):
  eye = eye(4)
  def __init__(self,expressionManager=None):
    fdl.graph.FrameGraph.__init__(self)
    self.expressionManager = expressionManager

