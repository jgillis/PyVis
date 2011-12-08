import types
from dymola.dymio import *
from dymola.simple import *
from numpy import *


#import ipdb

class StateManager:
  pass
  def isReady(self):
    return True

class TimeDependantStateManager(StateManager):
  def __init__(self,filename):
    pass

  def getT(t=None):
    if not(t is None):
      return t

  def getStates(t=None):
    pass


  def getDict(self,t):
    return dict(self.getStates(t),t=self.getT(t))


# Make this independent of timeManager
class FileStateManager(TimeDependantStateManager):
  def __init__(self,filename, timeManager=None):
    self.ann=AnnotatedDataModel(filename)
    self.timevec=self.ann.data['time'].data
    if not(timeManager is None) and hasattr(timeManager,'setTimeVec'):
      timeManager.setTimeVec(self.timevec)
    self.variables=dict()
    self.constants=dict()
    for k,v in self.ann.data.iteritems():
      if v.isConstant():
        self.constants[k] = v.data
      else:
        self.variables[k] = None # Existant, but no value yet

  def getT(self,t):
    if isinstance(t,types.IntType):
      return self.timevec[t]
    else:
      return t


  # problemas problemas  v.data should be nx3
  def getStates(self,t):
    if isinstance(t,types.IntType):
      for k,v in self.ann.iterSeries():
        self.variables[k] = v.data[...,t]
    else:
      for k,v in self.ann.iterSeries():
        c = v.data
        self.variables[k] = interp(t,self.timevec,c)
     
    
    return dict(self.constants,**self.variables)

  def getTimeVec(self):
    return self.timevec
    
class ExpressionStateManager(TimeDependantStateManager):
  def __init__(self,expressions):
    """
     A dict of (variable name -> Expression)
    """
    self.expressions = expressions

  def getT(self,t):
    return t

  def getStates(self,t):
    return dict([(key, value.value(t)) for key, value in self.expressions.iteritems()])
    
class InteractiveStateManager(StateManager):
  def configure(self,scene):
    self.variables = scene.fg.variables

class DummyStateManager(TimeDependantStateManager):
  def getT(self,t):
    return t
  def getStates(self,t):
    return {'phi':2*t,'theta':sin(t)}
    
    
