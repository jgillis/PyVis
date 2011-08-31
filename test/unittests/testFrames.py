from visualizer.expressions import *
from visualizer.states import *
from visualizer.frame import *
import fdl.primitives

sm = FileStateManager('result.txt')
em = ExpressionManager(sm)
em.addContext(fdl.primitives.__dict__)

fg=FrameGraph(em)
fg.config('sample.fdl',Frame)

f = fg.getFrame('p')

print f.getFrameMatrix(1.0)
print f.getFrameMatrix(0.2)

print f.matrix
print f.matrix.evaluate(0.2)
