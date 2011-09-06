from visualizer import *
from visualizer.vpython import *
import re
import inspect
import numpy

class Quickstart:
  pass
  
class QuickStartException:
  pass
  
def quickstart(*args,**kwargs):
  quickstarts = [AxesInteractiveFrames]
  for q in quickstarts:
    try:
      q.do(*args,**kwargs)
      break
    except QuickStartException as e:
      pass


class AxesInteractiveFrames(Quickstart):
  """

  Rx(alpha) tr(x,y,z)*Ry(beta) Rz(gamma)
  
  space is a seperator

  """
  @staticmethod
  def do(arg):
    if not(isinstance(arg,type(""))):
      raise QuickStartException()
    tm = RealTimeManager()
    sm = InteractiveStateManager()

    fg = FrameGraph()
    fg.config()

    frames = arg.split()
    f = fg.getWorldFrame()
    

    variables = []
    variabletypes = []
    
    context = numpy.__dict__
    import fdl.primitives
    context.update(fdl.primitives.__dict__)
    
    for fs in arg.split():
      f = fg.add(Frame(f,fs))
      for m in re.finditer("\w+", fs):
        match = m.group(0)
        print "mymatch = ", match
        if not(match in context) and not(match in variables):
          variables.append(match)
          bracketpos = fs[:m.start()].rfind("(")
          if bracketpos>2 and fs[bracketpos-2] == "R":
            variabletypes.append("angular")
          else:
            variabletypes.append("linear")

    for k,v in zip(variables,variabletypes):
      print k
      fg.add(Variable(k,type=v))

    s = Scene()
    s.config(fg, tm,sm)
    s.addAxes(Axes)

    s.start()
