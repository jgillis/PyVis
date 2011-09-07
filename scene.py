import visualizer.frame as visframe
from visualizer.expressions import *
import fdl.primitives

class Scene:
  fg=None
  objects=[]

  def __init__(self):
    pass
    
  def config(self,filename,timeManager,stateManager):
    self.stateManager=stateManager
    self.timeManager=timeManager
    self.expressionManager=ExpressionManager(timeManager,stateManager)
    self.fg=visframe.FrameGraph(self.expressionManager)
    self.fg.config(filename, visframe.Frame, visframe.WorldFrame)
    self.expressionManager.addContext(fdl.primitives.__dict__)
      
  def add(self,object):
    """
    
    Use to add a Frame
    
    """
    if isinstance(object,Frame):
      self.fg.add(object)
      
  def addAxes(self,AxesClass):
    colors = ['white','green','red','blue']
    
    for i,f in enumerate(self.fg.frames):
      print i, f, f.id
      self.addObject(f.id,AxesClass(color=colors[i % len(colors)]))
      
  def addObject(self,*args):
    """
    
    addObject(obj)
      obj get's added to world frame {0}
    
    addObject(frame, obj)
      frame must be an integer
    
    """
    if len(args)==1:
      frame=0
      obj=args[0]
    if len(args)==2:
      frame=args[0]
      obj=args[1]
    frame = self.fg.getFrame(frame)
    obj.addToScene(self,frame)
    self.objects.append(obj)

  def addFrame(self,*arg,**kwarg):
    arg[0] = fg.getFrame(arg[0]) # special treatement for the baseframe
    self.fg.add(Frame(*arg,**kwarg))

  def getWorldFrame(self):
    return fg.getWorldFrame()
      
  def start(self):
    """
    The main loop that does the drawing. Never returns
    """
    if hasattr(self.stateManager,'configure'):
      self.stateManager.configure(self)
    if hasattr(self.stateManager,'draw'):
      self.stateManager.draw()
      
    if hasattr(self.timeManager,'draw'):
      self.timeManager.draw()
    if hasattr(self.timeManager,'configure'):
      self.timeManager.configure(self)
      
    while True:
      if hasattr(self.timeManager,'mainloop'):
        self.timeManager.mainloop()
      t = self.timeManager.getTime()
      if hasattr(self.stateManager,'mainloop'):
        self.stateManager.mainloop()
      for o in self.objects:
        o.update(t)

