#plot.py

import matplotlib
from mpl_toolkits.mplot3d import Axes3D
import numpy,time
import matplotlib.pyplot as pyplot

from shared import *


class plotFigure:
	"class to deal with plotting of 3D line graphs"

	def __init__(self,data,filename):

		currentTime = str(int(time.time()))
		currentTime = int(currentTime[-4:])
		"output/plot_output_{}.png".format(currentTime)

		self.filename = filename
		self.loadData(data.getData())

	def loadData(self,inputData):
		"method to load plotting data into the class variabales"

		self.x,self.y,self.z = inputData[0],inputData[1],inputData[2]

	def plot(self,seriesTitle,show=False):
		"method to plot the class data and if DEBUG = False save the figure"

		matplotlib.rcParams['legend.fontsize'] = 10

		fig = pyplot.figure()
		ax = fig.gca(projection='3d')

		x,y,z = self.x,self.y,self.z
		
		ax.plot(x, y, z, label=seriesTitle)
		ax.legend()

		if show:
			pyplot.show()
		
		pyplot.savefig(self.filename)