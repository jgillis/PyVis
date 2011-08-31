# -*- coding: utf-8 -*-
from numpy import *
# Run as: python sample.py

#execfile('visualize.py');

from vpythonvisualizer import *

scene=vpythonvisualizer()

scene.config('config.fdl');

def myFrame(t,state):
	alpha = state['alpha']
	return TRx(alpa)

scene.addFrame('world',myFrame,name='myframe');

scene.getFrame('world')

arrow(scene.getFrame('world'),scene.getFrame('world'))

class myObject(PrimitiveCollection):
  	def __init__(self,T=None):
    		PrimitiveCollection.__init__(self,T)
    		self.primitives=[
       		Text(self.frame,text='Joby')
    		]
	

def myObject(t,state):
	[template.axes(),template.airplane()]

scene.addObject('world',[template.axes(color=color.white, length='alpha')]);
scene.addObject('world',myObject);

scene.addObject('world',Box(x='alpha',y='beta',z='{saf}'))



[template.axes(),template.airplane()]



scene.loadTimeSeries('res.txt');
scene.debug();

