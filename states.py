import types
from dymola.dymio import *
from numpy import *


class StateManager:
  pass
  

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
    self.dym=ResultDymolaTextual(filename)
    self.timevec=self.dym.data[1][:,0]
    if not(timeManager is None) and hasattr(timeManager,'setTimeVec'):
      timeManager.setTimeVec(self.timevec)
    self.variables=dict()
    for i in range(len(self.dym.name)):
      if self.dym.dataInfo[i,0]==2:
        self.variables[self.dym.name[i]] = None

    self.constants=dict()
    for i in range(len(self.dym.name)):
      if self.dym.dataInfo[i,0]==1:
        self.constants[self.dym.name[i]] = self.dym.data[0][0,self.dym.dataInfo[i,1]-1]

  def getT(self,t):
    if isinstance(t,types.IntType):
      return self.timevec[t]
    else:
      return t

  def getStates(self,t):
    if isinstance(t,types.IntType):
      for k in self.variables.keys():
        self.variables[k] = self.dym.data[1][t,self.dym.get_column(k)]
        c = self.dym.data[1][:,self.dym.get_column(k)-1]
    else:
      for k in self.variables.keys():
        c = self.dym.data[1][:,self.dym.get_column(k)-1]
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
  def __init__(self,variables):
     """
      Variables is a dict with the signature as found in fdl
      or the name of an fdl file
     """
     from fdl.parser import fdl
     if isinstance(variables,type("")):
       self.fdl = fdl(variables)
       self.variables = self.fdl.tree['variables']
     else: 
       self.variables = variables

class DummyStateManager(TimeDependantStateManager):
  def getT(self,t):
    return t
  def getStates(self,t):
    return {'phi':2*t,'theta':sin(t)}
    
    
