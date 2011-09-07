from visualizer import *
from visualizer.vpython import *

"""
Demonstrates how you can avoid using fdl files.
"""

tm = RealTimeManager()
em = ExpressionManager(tm)

sm = ExpressionStateManager({'gamma' : em('4*t'), 'alpha' : em('0.4*t'), 'x' : em('2'),'beta': em('0.5'),'y': em('2'), 'z': em('2')})



fg = FrameGraph()
fg.config()

w = fg.getWorldFrame()
f = fg.add(Frame(w,'tr(0,0,x)'))
f = fg.add(Frame(f,'Rz(alpha)'))
f = fg.add(Frame(f,'Rx(beta)'))
f = fg.add(Frame(f,'tr(0,0,y)'))
f = fg.add(Frame(f,'Rz(gamma)'))
f = fg.add(Frame(f,'tr(0,0,z)'))

fg.add(Variable())

s = Scene()

s.config(fg, tm,sm)
s.addAxes(Axes)
s.addObject(5,Trace(dx=1,dy=0,dz=0,color='red'))
s.addObject(5,Trace(dx=1,dy=0,dz=0,color='green',wrt=2,L=40))



#s.addObject(5,Vector(dx=0,dy=0.5,dz=0.8,color='blue',e=0))  # Plot a vector expressed in frame {e}, put it's base at the origin of frame {5}

d = Displacement(dx=0,dy=0,dz=0.5,e=0)
d2 = Displacement(dx=0,dy=0,dz=0.8,e=0)



s.addObject(5,Vector(T=tr(0.5,0,0),d=d,color='red'))
s.addObject(5,Vector(T=tr(0.7,0,0),d=d2,color='blue'))
s.addObject(5,Vector(T=tr(0.9,0,0),d=d+d2,color='blue'))
#s.addObject(5,Vector(T=tr(1.1,0,0),b=d,d=d2,color='green'))
s.addObject(6,Vector(T=tr(0,0.5,0),dx=0.5,dy=0,dz=0,color='yellow',e=2))

d = Displacement(dx=0,dy=0.5,dz=0) + Displacement(dx=0.5,dy=0,dz=0,e=2)

s.addObject(6,Trace(d=d,color='yellow',wrt=0,L=40)) # Task: trace out the head of the yellow arrow.

s.addObject(6,Trace(d=d,color='yellow',wrt=2,L=40)) # Task: trace out the head of the yellow arrow.


s.start()
