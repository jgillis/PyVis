from visualizer import *
from visualizer.vpython import *
import re
import inspect
import numpy
import types
import imp
import warnings
import ipdb

class QuickstartException(Exception):
  pass
  
def getFunction(arg):
  """
  
  getFunction(myfun)
  getFunction("myfile.py:myfunction")
  
  """
  if isinstance(arg,types.FunctionType):
    return arg
  elif isinstance(arg,types.StringType):
    try:
      (myfile,myfunction) = arg.split(":")
    except:
      raise QuickstartException("getFunction(%s): expecting 'myfile.py:myfunction'" % arg)
  else:
    raise QuickstartException("getFunction(%s): unknown argument type" % arg)
  with warnings.catch_warnings(record=True) as w:
    mod = imp.load_source('module.name', myfile)
  if not(hasattr(mod,myfunction)):
    raise Exception("getFunction(%s): cannot find %s in %s " % (arg,myfunction,mymodule))
  else:
    return getattr(mod,myfunction)
    
def getDymFile(arg):
  """
  getDymFile("myfile.dym")
  """
  if not(isinstance(arg,types.StringType)):
    raise QuickstartException("getDymFile(%s): argument must be string " % arg)
  if not(arg.endswith('.dym')):
    raise QuickstartException("getDymFile(%s): argument mustend on dym " % arg)
  return arg
  
def getFdl(arg):
  """
  getFdl("myfile.fdl")
  """
  if not(isinstance(arg,types.StringType)):
    raise QuickstartException("getFdl(%s): argument must be string " % arg)
  if not(arg.endswith('.fdl')):
    raise QuickstartException("getFdl(%s): argument mustend on fdl " % arg)
  return arg
    
def getFg(arg):
  """
  getFg("Rx(alpha) tr(x,y,z)*Ry(beta) Rz(gamma)")
  """
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
  return fg


  
def quickstart(*args,**kwargs):
  quickstarts = [("fdl",getFdl),("decorator",getFunction),("dymfile",getDymFile),("fg",getFg)]
  
  meta = {}
  for arg in args:
    for q,f in quickstarts:
      try:
        meta[q] = f(arg)
        break
      except QuickstartException:
        pass
        

  if 'dymfile' in meta:
    tm = FixedTimeManager()
    sm = FileStateManager(meta['dymfile'])
    tm.setTimeVec(sm.getTimeVec());
  else:
    tm = RealTimeManager()
    sm = InteractiveStateManager()

  s = Scene()
  if 'fdl' in meta:
    s.config(meta['fdl'], tm, sm)
  elif 'fg' in meta:
    s.config(meta['fg'], tm, sm)
    
  if 'decorator' in meta:
    meta['decorator'](s) 
  else:
    s.addAxes(Axes)

  s.start()
  
  for q in quickstarts:
    try:
      q.do(*args,**kwargs)
      break
    except QuickStartException as e:
      pass

