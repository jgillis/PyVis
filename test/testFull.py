from visualizer.vpython.graphics import *
from visualizer import *
from visualizer.states import *
from visualizer.vpython.time import *
from visualizer.scene import *

t = FixedTimeManager()
sm = FileStateManager('result.txt')
t.setTimeVec(sm.getTimeVec());

s = Scene()
s.setTimeManager(t)
s.config('sample.fdl',sm)

b = Box()
s.addObject('p',b)


s.start()
