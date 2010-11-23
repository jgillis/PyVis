from visualizer.states import *

class ExpressionManager:
  cache = dict()
  def __init__(self,stateManager):
    self.stateManager = stateManager
    self.context=dict()
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
      return 2
    if isinstance(expr,types.StringType):
      if expr.startswith('{') and expr.endswith('}'):
        return 1
    return 0
    
  def addContext(self,context):
    self.context.update(context)


#interpolation is possible (since we know what states are angular, we can unwrap them)

class Expression:
  def __init__(self,expressionManager,expr,force=None):
    self.expressionManager=expressionManager
    self.stateManager=self.expressionManager.stateManager
    if not(force is None):
      self.type = force
      self.expr = expr
    else:
      self.type = expressionManager.type(expr)
      if self.type == 1:
        self.expr = expr[1:-1]
      else:
        self.expr = expr

  def evaluate(self,t=None):
    if self.type==0:
      return self.expr
    elif self.type==2:
      return self.expr(self.stateManager.getT(t),self.stateManager.getStates(t))
    elif self.type==1:
      return eval(self.expr,self.stateManager.getDict(t),self.expressionManager.context)

  # caching functionality
  def value(self,t=None):
    if self.type == 0:
      return self.expr
    if not(t is None) and self.expressionManager.hasCache(self,t):
      return self.expressionManager.getCache(self,t)
    return self.evaluate(t)
  
  def __str__(self):
    return "{%s : %s}" % (self.type, str(self.expr))
