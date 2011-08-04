import visualizer.time
from visual.controls import *
import visual.controls

class InteractiveStateManager(visualizer.states.InteractiveStateManager):
  def draw(self):
  
    self.sliders=[]
    spacing = 40
    posy = 0
    
    w = 200

    self.c = controls(x=0, y=0, width=w, height=w, range=100)
    for v in self.variables:
      self.sliders.append(slider(pos=(-15,posy), width=7, length=70, axis=(1,0,0)))
      posy+=spacing
    
    button(pos=(-60,30), height=30, width=40, text='reset' , action=lambda: self.reset())

  def getT(self,t):
    if isinstance(t,types.IntType):
      return self.timevec[t]
    else:
      return t

  def getStates(self,t):
    [x.value for x in self.sliders]self.sliders.value
    
    if isinstance(t,types.IntType):
      for k in self.variables.keys():
        self.variables[k] = self.dym.data[1][t,self.dym.get_column(k)]
        c = self.dym.data[1][:,self.dym.get_column(k)-1]
    else:
      for k in self.variables.keys():
        c = self.dym.data[1][:,self.dym.get_column(k)-1]
        self.variables[k] = interp(t,self.timevec,c)
    return readFromSliders()

  def getTimeVec(self):
    return self.timevec
    
  def reset(self):
    states = {}
    for v in self.variables:
      default = 0
      if 'default' in v:
        default = eval(v['default'])
      elif 'bounds' in v:
        default = (eval(v['bounds'][0]) + eval(v['bounds'][1]))/2.0
      states[v.name] = default 
    writeToSliders(self,states)
    
  def readFromSliders(self):
    """
    Return a dict (variable name -> value)
    """
    ret= {}
    for i in len(self.variables):
      ret[self.variables[i].name] = self.sliders[i].value

  def writeToSliders(self,states):
    """
    Expects a dict (variable name -> value)
    """
    for i in len(self.variables):
      self.sliders[i] = states[self.variables[i].name]

  def mainloop(self):
    self.c.interact()
    self.advance()
    
  def register(self,manager):
    manager.addToMainLoop(self.mainloop)
