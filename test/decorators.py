from visualizer import *
from visualizer.vpython import *

def foo(s):
  s.addObject(0,Cylinder(r=1,h=0.1,color='red'))
  s.addObject(1,Cylinder(r=0.2,h=1))
  s.addObject(2,Box(x=0.1,y=0.1,z=2))
