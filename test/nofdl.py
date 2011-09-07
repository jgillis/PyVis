from visualizer import *
from visualizer.vpython import *

"""
Demonstrates how you can avoid using fdl files.
"""

tm = RealTimeManager()
sm = InteractiveStateManager()

fg = FrameGraph()
fg.config()

w = fg.getWorldFrame()
f = fg.add(Frame(w,'Rx(psi)'))
f = fg.add(Frame(f,'tr(0,0,x)'))
f = fg.add(Frame(f,'Ry(alpha)'))

fg.add(Variable("psi",type="angular"))
fg.add(Variable("alpha",type="angular"))
fg.add(Variable("x",type="linear"))

s = Scene()

s.config(fg, tm,sm)

s.addObject(0,Axes(color='green'))
s.addObject(1,Axes(color='red'))
s.addObject(2,Axes(color='blue'))
s.addObject(3,Axes(color='white'))

s.start()
