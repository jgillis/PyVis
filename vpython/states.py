import visualizer.states
import visual.controls as controls
import types

import ipdb

class InteractiveStateManager(visualizer.states.InteractiveStateManager):
  def draw(self):
  
    
    self.sliders=[]
    self.slidercaptions = []
    
    
    
    w = 500.0
    
    spacing_px = 40.0
    
    button_px = 100
    
    marginbottom_px = 20.0
    margintop_px = 20.0
    button_area_px = 100.0
    button_height_px = 80
    
    
    
    r= 100.0
    
    h = len(self.variables)*spacing_px + marginbottom_px + margintop_px + button_area_px + button_height_px
    
    posy = -r/2 + marginbottom_px/h*r
    spacing = (spacing_px / h) * r
    

    self.c = controls.controls(x=0, y=0, width=w, height=h, range=r)
    for v in self.variables:
      s = controls.slider(pos=(-15,posy), width=7, length=70, axis=(1,0,0))
      
      s.value = v["default"]
      s.min,s.max = v["bounds"]
      
      sc = controls.label(text=v["name"],align='right', pos=(r*(-0.5+0.1),posy),display=self.c.display,box = False )
      self.sliders.append(s)
      self.slidercaptions.append(sc)
      print posy
      posy+=spacing
    
    controls.button(pos=(0,r*(0.5-button_area_px/h)), height=button_height_px/h*r, width=r/2, text='reset' , action=lambda: self.reset())

  def getT(self,t):
    if isinstance(t,types.IntType):
      return self.timevec[t]
    else:
      return t

  def getStates(self,t):
    #[x.value for x in self.sliders]self.sliders.value
    #ipdb.set_trace()
    
    #if isinstance(t,types.IntType):
    #  for variable in self.variables:
    #    self.variables[k] = self.dym.data[1][t,self.dym.get_column(k)]
    #    c = self.dym.data[1][:,self.dym.get_column(k)-1]
    #else:
    #  for k in self.variables.keys():
    #    c = self.dym.data[1][:,self.dym.get_column(k)-1]
    #    self.variables[k] = interp(t,self.timevec,c)
    return self.readFromSliders()

  def getTimeVec(self):
    return self.timevec
    
  def reset(self):
    states = {}
    for v in self.variables:
      default = 0
      states[v["name"]] = v["default"]
    self.writeToSliders(states)
    
  def readFromSliders(self):
    """
    Return a dict (variable name -> value)
    """
    ret= {}
    for (i,variable) in enumerate(self.variables):
      ret[variable["name"]] = self.sliders[i].value
      self.slidercaptions[i].text = variable["name"] + ": %.4f" %  self.sliders[i].value
   
    return ret

  def writeToSliders(self,states):
    """
    Expects a dict (variable name -> value)
    """
    for (i,variable) in enumerate(self.variables):
      self.sliders[i].value = states[variable["name"]]
      

  def mainloop(self):
    self.c.interact()
    
  def register(self,manager):
    manager.addToMainLoop(self.mainloop)
