from graphics import *
from vpythonvisualizer import *
from states import *

sm = FileStateManager('result.txt')

s = Scene()
print 132
s.config('sample.fdl',sm)

b = Box()
s.addObject('world',b)

