from visualizer.states import *
import numpy

class ExpressionManager:
  cache = dict()
  def __init__(self,timeManager,stateManager=None):
    """
    manager can be a stateManager or TimeManager
    """
    
    self.stateManager = stateManager
    self.timeManager  = timeManager
    
    self.context=numpy.__dict__
    
  def createExpression(self,expr,force=None):
    return Expression(self,expr,force)

  def hasCache(self,expr,t=None):
    return False

  @staticmethod
  def type(expr):
    """
    returns:
    0 - literal
    1 - expression
    2 - function
    """
    if isinstance(expr,types.FunctionType):
      return (2,expr)
    if isinstance(expr,types.StringType):
      if expr.startswith('"') and expr.endswith('"'):
        return (0,expr[1:-1])
      return (1,expr)
    return (0,expr)
    
  def addContext(self,context):
    self.context.update(context)
    
  __call__ = createExpression

#interpolation is possible (since we know what states are angular, we can unwrap them)

class Expression:
  def __init__(self,expressionManager,expr,force=None):
    self.expressionManager=expressionManager
    self.stateManager=self.expressionManager.stateManager
    self.timeManager=self.expressionManager.timeManager
    if not(force is None):
      self.type = force
      self.expr = expr
    else:
      self.type, self.expr = expressionManager.type(expr)

  def evaluate(self,t=None):
    if t is None:
      t=self.timeManager.getTime()
    if self.type==0:
      return self.expr
    elif self.type==2:
      if self.stateManager is None:
       return self.expr(t)
      else:
       return self.expr(t,self.stateManager.getStates(t))
       
    elif self.type==1:
      d = {'t' : t}
      if not(self.stateManager is None):
        d.update(self.stateManager.getStates(t))
      return eval(self.expr,d,self.expressionManager.context)

  # caching functionality
  def value(self,t=None):
    if self.type == 0:
      return self.expr
    if not(t is None) and self.expressionManager.hasCache(self,t):
      return self.expressionManager.getCache(self,t)
    return self.evaluate(t)
  
  def __str__(self):
    return "{%s : %s}" % (self.type, str(self.expr))
    
  __call__ = value
