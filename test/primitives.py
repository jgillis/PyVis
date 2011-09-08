from visualizer.quickstart import *

def dec(s):
  s.addObject(0,Axes(color='white'))
  s.addObject(0,Box(x=1,y=1,z=1,color='green'))
  s.addObject(1,Box(x=1,y=1,z=1,T=tr(0,0,1),color='red'))
  s.addObject(1,Box(x=1,y=1,z=1,T=Ry(pi),color='blue'))
  
quickstart("tr(2,0,0) tr(2,0,0) tr(2,0,0)",dec)
