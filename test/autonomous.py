from visualizer import *
from visualizer.vpython import *

tm = RealTimeManager()
em = ExpressionManager(tm)

sm = ExpressionStateManager({'psi' : em('t'), 'alpha' : em('0.1*sin(t)'), 'x' : em('cos(t)')})

s = Scene()
s.config('sample.fdl', tm,sm)

s.addObject(0,Cylinder(r=1,h=0.1,color='red'))

s.addObject(1,Cylinder(r=0.2,h=1))
s.addObject(1,Box(x=1,y=1,z=0.1))
s.addObject(0,Box(x=1,y=1,z=0.1,T='tr(x,0,0)'))


#p.add([Arrow(x=1,y=0,z=0), Arrow(x=0,y=1,z=0), Arrow(x=0,y=0,z=1)])



s.addObject(1,Trace(dx=0,dy=0,dz=2))


s.addObject(2,Box(x=0.1,y=0.1,z=0.1,T='tr(1,0,0)'))
s.addObject(2,Trace(dx=1,dy=0,dz=0))


s.addObject(1,Arrow(x=1,y=0,z=2,color=(0.2,0.4,0.7)))
s.addObject(1,Axes(color='green'))

p = PrimitiveCollection(T='tr(x,0,x)')
p.add(Box(x=1,y=1,z=0.1,T='tr(0,0,-2)'))
p.add(Box(x=1,y=1,z=0.1,T='tr(0,0,-4)'))
p.add(Axes(T='tr(0,0,-4)'))
s.addObject(0,p)

s.start()
