from expressions import *
from states import *

sm = FileStateManager('result.txt')
em = ExpressionManager(sm)



print em.createExpression('{psi}').value(1.0)
print em.createExpression('psi').value(1.0)
print em.createExpression('psi',force = 1).value(1.0)
print em.createExpression('psi',force = 1).value(1.1)


def myfunction(t,d):
  return d['psi']
  
print em.createExpression(myfunction).value(1.1)

print em.createExpression(2).value(1.1)
