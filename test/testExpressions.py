from visualizer.expressions import *
from visualizer.states import *
from visualizer.time import *

tm = RealTimeManager()

print "The time is %.8f [s]" % tm()

sm = FileStateManager('result.txt',tm)
em = ExpressionManager(tm,sm)

somevar = em.createExpression('5*t')

print "Printing somevar: ", somevar      
print "Evaluating at a particular time: ", somevar(1.0)
print "Evaluating at the current time: ", somevar()

print "Evaluating at a particular time; full syntax: ", somevar.value(1.0)
print "Evaluating at the current time; full syntax: ", somevar.value()

print em('t').value(1.0)
print em('psi').value(1.0)
print em('"psi"').value(1.0)
print em('psi',force = 1).value(1.0)
print em('psi',force = 1).value(1.1)

def myfunction(t,d):
  return d['psi']
  
print em(myfunction).value(1.1)

print em(2).value(1.1)



print "Testing the ExpressionStateManager"
tm = RealTimeManager()
em = ExpressionManager(tm)

sm = ExpressionStateManager({'psi' : em('t'), 'alpha' : em('0.1*sin(t)'), 'x' : em('cos(t)')})

em = ExpressionManager(tm,sm)

print em('psi').value(1.0)
print em('t').value(1.0)
print em('psi').value()
print em('t').value()
