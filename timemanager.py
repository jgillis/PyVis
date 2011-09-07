from __future__ import absolute_import
from numpy import prod,floor
import time
import types
  
class TimeManager:
  # should be able to output floats and int according to discretised flag
  
  def __call__(self):
    return self.getT()
    
  def getT(self):
    return t


class RealTimeManager(TimeManager):
  def __init__(self):
    self.starttime = time.time()
  def getT(self):
    return time.time()-self.starttime
  getTime = getT
  
class FixedTimeManager(TimeManager):
  def setTimeVec(self,vec):
    self.timevec = vec
    self.npoints = prod(vec.shape)
    self.discrete=True
    self.pause = False
    self.setDiscrete()

  def initcheck(self):
    if not(hasattr(self,'timevec')):
      raise Exception("FixedTimeManager has not been initialised")
      
  
  def getTimeVec(self):
    return self.timevec

  def getT(self,t=None):
    if isinstance(t,types.IntType):
      return self.timevec[t]
    elif t is None:
      return 0
    else:
      return t
      
  def getTime(self):
    if self.type==0:
      return self.index
    else:
      return self.T
      
      
  def setIndex(self,value):
    self.index = value
    self.floatindex = value
  def setDiscrete(self,step=1):
    self.type=0
    self.step=1
    self.index=0
    self.floatindex=0    
   
  def advance(self,step=None):
    """
    Step can be fractional
    """
    if self.pause or not(hasattr(self,'timevec')):
      return
    if step is None:
      step=self.step
    self.floatindex += step
    self.index = int(self.floatindex)
    while self.index >= self.npoints:
      self.index -= self.npoints
      self.floatindex -= self.npoints
