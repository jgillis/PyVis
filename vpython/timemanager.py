import visualizer.timemanager
import visual
import visual.controls as controls

class FixedTimeManager(visualizer.timemanager.FixedTimeManager):
  def draw(self):
    w = 200
    self.c = controls.controls(x=0, y=0, width=w, height=w, range=100)
    controls.button(pos=(-60,30), height=30, width=40, text='<<' , action=lambda: self.first())
    controls.toggle(pos=(0,30),height=30, width=40, text='Pause', action=lambda: self.pauseToggle())
    controls.button(pos=(60,30), height=30, width=40, text='>>',action= lambda: self.last())
    
    self.timelabel = controls.label(pos=(-15,-55),display=self.c.display)
    self.s1=controls.slider(pos=(-15,-30), width=7, length=70, axis=(1,0,0), action=lambda: self.slider1())
    self.s1.value = 0
    
    self.s2=controls.slider(pos=(-15,80),min=-1,max=3, width=7, length=70, axis=(1,0,0),action=lambda: self.slider2())
    self.s2.value = 0
    
    
    self.pause = False
    self.advancestep = 1

  def first(self):
    self.setIndex(0)
    
  def last(self):
    self.setIndex(self.npoints-1)
    
  def pauseToggle(self):
    self.pause = not(self.pause)
    
  def slider1(self):
    if self.pause:
      self.sliderposTostate(self.s1.value)
  
  def slider2(self):
    self.advancestep = 10.0**(self.s2.value)
      
  def sliderposTostate(self,value):
    if self.type==0:
      self.setIndex(int(value /100.0 * (self.npoints-1)))
    else:
      self.T = value /100.0 * self.timvec[-1]
      
  def sliderposFromstate(self):
    if self.type==0:
      return self.index/(self.npoints-1.0) * 100
    else:
      return self.T/(self.timvec[-1]+0.0)* 100
      
  def register(self,manager):
    manager.addToMainLoop(self.mainloop)
    
    
  def debug(self,*args,**kwargs):
    print args
    print kwargs
  
  def showIndex(self):
    self.timelabel.text = str(self.index)
    
  def mainloop(self):
    self.c.interact()
    visual.rate(40)
    self.advance(self.advancestep)
    self.s1.value = self.sliderposFromstate()
    self.showIndex()
