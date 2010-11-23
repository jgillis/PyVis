from numpy import prod

class TimeManager:
  # should be able to autput floats and int according to discretised flag
  def getT(self):
    return t


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

  def setDiscrete(self,step=1):
    self.type=0
    self.step=1
    self.index=0    
   
  def advance(self,step=None):
    if self.pause or not(hasattr(self,'timevec')):
      return
    if step is None:
      step=self.step
    self.index += step
    while self.index >= self.npoints:
      self.index -= self.npoints
