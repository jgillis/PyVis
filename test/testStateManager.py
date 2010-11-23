from visualizer.states import *

sm = FileStateManager('result.txt')

print "Time goes from %e to %e" % (sm.getT(0),sm.getT(-1))


print sm.getStates(0)

print sm.getDict(1)

print sm.getDict(1.0)
print sm.getDict(1.1)
