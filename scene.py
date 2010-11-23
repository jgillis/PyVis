from Frame import *
	
from expressions import *
import fdl.primitives

class Scene:
  fg=None
  objects=[]

  def __init__(self):
    pass
    
  def config(self,filename,stateManager):
    self.stateManager=stateManager
    self.expressionManager=ExpressionManager(stateManager)
    self.fg=FrameGraph(self.expressionManager)
    self.fg.config(filename, Frame, WorldFrame)
    self.expressionManager.addContext(fdl.primitives.__dict__)
      
  def add(self,object):
    if isinstance(object,Frame):
      self.fg.add(object)
      
  def addObject(self,*args):
    if len(args)==1:
      frame=0
      obj=args[0]
    if len(args)==2:
      frame=args[0]
      obj=args[1]
    obj.addToScene(self,frame)
    self.objects.append(obj)

  def addFrame(self,*arg,**kwarg):
    arg[0] = fg.getFrame(arg[0]) # special treatement for the baseframe
    self.fg.add(Frame(*arg,**kwarg))

  def getWorldFrame(self):
    return fg.getWorldFrame()

