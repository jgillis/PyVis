class TimeManager:
  # should be able to autput floats and int according to discretised flag
  def getT(self):
    return t


class FixedTimeManager(TimeManager):
  def setTimeVec(self,vec):
    self.timevec = vec
    self.npoints = vec.shape[0] * vec.shape[1]

  def initcheck(self):
    if not(hasattr(self,timevec)):
      raise Exception("FixedTimeManager has not been initialised")
    if not(hasattr(self,type)):
      self.setDiscrete()
      
  
  def getTimeVec(self):
    return self.timevec

  def getT(self,t=None):
    if isinstance(t,types.IntType):
      return self.timevec[t]
    elif t is None:
      return 0
    else:
      return t

  def setDiscrete(step=1):
    self.type=0
    self.step=1
    self.index=0    
   
  def advance(self,step=self.step):
    self.index += self.step
    while self.index >= len(self.npoints):
      self.index -= len(self.npoints)
