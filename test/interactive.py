from visualizer import *
from visualizer.vpython import *

tm = RealTimeManager()

sm = InteractiveStateManager('interactive.fdl')

s = Scene()
s.config('interactive.fdl', tm,sm)

s.addObject(0,Axes(color='green'))
s.addObject(1,Axes(color='blue'))
s.addObject(2,Axes(color='red'))
s.addObject(3,Axes(color='white'))

s.start()
