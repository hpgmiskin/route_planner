import numpy,matplotlib
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot

FONTSIZE = 10

def saveFigure(title,show):
	"function to save or show the current figure given the title"

	if show:
		pyplot.show()
		pyplot.close()
		return None
	else:
		filename = "figures/{}.png".format(title.replace(" ","_").lower())
		pyplot.savefig(filename)
		pyplot.close("all")
		return filename

def histogram(data,title="",xLabel="Value",yLabel="Frequency",lines=None,numberBars=10,show=False):
	"plots a histogram of the given data data"

	maxFrequency = len(data)/numberBars

	pyplot.figure(num=title)
	pyplot.hold(True)
	pyplot.hist(data,numberBars)
	pyplot.title(title,fontsize=FONTSIZE)
	pyplot.xlabel(xLabel,fontsize=FONTSIZE)
	pyplot.ylabel(yLabel,fontsize=FONTSIZE)

	if lines:
		for name,line in sorted(lines.items(),key=lambda x:x[0],reverse=True):
			pyplot.plot([line,line],[0,maxFrequency],label=name,linewidth=0.5)
		pyplot.legend()

	pyplot.hold(False)

	return saveFigure(title,show)

def bar(labels,values,title="",xLabel="",yLabel="",show=False):
	"plots a bar chart with the givne labels and data values"

	length = len(values)

	indexs = numpy.arange(length)
	barWidth = 1

	figure = pyplot.figure(num=title)
	axes = pyplot.axes()

	barAxes = pyplot.bar(indexs,values,barWidth)

	pyplot.legend(barAxes,labels,fontsize=FONTSIZE)
	pyplot.title(title,fontsize=FONTSIZE)

	labels = [label[:10] for label in labels]
	pyplot.xticks(indexs + barWidth/2, labels, rotation=0)
	pyplot.yticks(range(0,max(values)+10,5))
	
	pyplot.xlabel(xLabel,fontsize=FONTSIZE)
	pyplot.ylabel(yLabel,fontsize=FONTSIZE)

	return saveFigure(title,show)

def pie(labels,values,title="",xLabel="",yLabel="",show=False):
	"plot a pie cahrt with the given labels and data values"

	figure = pyplot.figure(num=title)
	axes = pyplot.axes()

	pyplot.pie(values, labels=[label[:10] for label in labels])
	pyplot.legend(labels,fontsize=FONTSIZE)
	pyplot.title(title,fontsize=FONTSIZE)

	pyplot.xlabel(xLabel,fontsize=FONTSIZE)
	pyplot.ylabel(yLabel,fontsize=FONTSIZE)

	return saveFigure(title,show)

def line(xAxis,yAxis,title="",xLabel="",yLabel="",xTicks=None,yTicks=None,show=False):
	"method to plot the class data and if DEBUG = False save the figure"

	pyplot.figure(num=title)
	pyplot.hold(True)
	pyplot.title(title)

	if (type(xAxis[0]) == str):
		xTicks = xAxis
		xAxis = numpy.arange(len(xAxis))

	if (type(yAxis) == dict):
		yMin,yMax = 0,0
		for name,data in sorted(yAxis.items(),key=lambda x:x[0]):
			yMin = min(data+[yMin])
			yMax = max(data+[yMax])
			pyplot.plot(xAxis[:len(data)],data[:len(xAxis)],label=name)
	elif (type(yAxis) == list):
		yMin = min(yAxis)
		yMax = max(yAxis)
		pyplot.plot(xAxis[:len(yAxis)],yAxis[:len(xAxis)],label="")
	else:
		raise ValueError("Plot expected list or dictionary for yAxis")

	if xTicks:
		pyplot.xticks(xAxis, xTicks, rotation=0)

	pyplot.xlabel(xLabel,fontsize=FONTSIZE)
	pyplot.ylabel(yLabel,fontsize=FONTSIZE)
	ySpace = (yMax-yMin)*0.05
	pyplot.ylim((yMin-ySpace,yMax+ySpace))
	pyplot.legend(fontsize=FONTSIZE)
	pyplot.hold(False)

	return saveFigure(title,show)

def line3(xAxis,yAxis,zAxis,title="",xLabel="x",yLabel="y",zLabel="z",show=False):
	"method to plot the class data and if DEBUG = False save the figure"

	matplotlib.rcParams['legend.fontsize'] = 10

	figure = pyplot.figure(num=title)
	axes = Axes3D(figure)

	axes.plot(xAxis, yAxis, zAxis, label=title)
	axes.set_xlabel(xLabel,fontsize=FONTSIZE)
	axes.set_ylabel(yLabel,fontsize=FONTSIZE)
	axes.set_zlabel(zLabel,fontsize=FONTSIZE)
	axes.set_title(title,fontsize=FONTSIZE)
	axes.legend()

	return saveFigure(title,show)

def path(paths,title="",xLabel="x",yLabel="y",arrows=None,show=False):
	"function to plot the given paths"

	figure = pyplot.figure(num=title)
	axes = pyplot.axes()
	pyplot.hold(True)
	pyplot.title(title)

	for label,data in paths.items():
		[x,y,z] = data
		axes.plot(x[:len(y)],y[:len(x)],label=label)

	if arrows:
		for label,data in arrows.items():
			[x1,y1,x2,y2] = data
			axes.arrow(x1,y1,x2,y2,head_width=0.1, fc='k', ec='k')

	axes.set_xlabel(xLabel,fontsize=FONTSIZE)
	axes.set_ylabel(yLabel,fontsize=FONTSIZE)
	axes.set_title(title,fontsize=FONTSIZE)
	axes.legend()
	pyplot.hold(False)
	pyplot.axis('equal')

	return saveFigure(title,show)

def path3(paths,title="",xLabel="x",yLabel="y",zLabel="z",show=False):
	"method to plot the class data and if DEBUG = False save the figure"

	matplotlib.rcParams['legend.fontsize'] = 10

	figure = pyplot.figure(num=title)
	pyplot.hold(True)
	axes = Axes3D(figure)

	for label,data in paths.items():
		[x,y,z] = data
		axes.plot(x, y, z, label=label)

	pyplot.hold(False)
	axes.set_xlabel(xLabel,fontsize=FONTSIZE)
	axes.set_ylabel(yLabel,fontsize=FONTSIZE)
	axes.set_zlabel(zLabel,fontsize=FONTSIZE)
	axes.set_title(title,fontsize=FONTSIZE)
	axes.legend()

	return saveFigure(title,show)

def scatter(xAxis,yAxis,title="",xLabel="x",yLabel="y",xTicks=None,yTicks=None,show=False):
	"method to plot the class data and if DEBUG = False save the figure"

	pyplot.figure(num=title)
	pyplot.hold(True)
	pyplot.title(title,fontsize=FONTSIZE)

	if (type(xAxis[0]) == str):
		xTicks = xAxis
		xAxis = numpy.arange(len(xAxis))

	if (type(yAxis) == dict):
		for name,data in sorted(yAxis.items(),key=lambda x:x[0]):
			pyplot.scatter(xAxis[:len(data)],data[:len(xAxis)],label=name)
	elif (type(yAxis) == list):
		pyplot.scatter(xAxis[:len(yAxis)],yAxis[:len(xAxis)],label="")
	else:
		raise ValueError("Plot expected list or dictionary for yAxis")

	if xTicks:
		pyplot.xticks(xAxis, xTicks, rotation=0)

	pyplot.xlabel(xLabel,fontsize=FONTSIZE)
	pyplot.ylabel(yLabel,fontsize=FONTSIZE)
	pyplot.legend(fontsize=FONTSIZE)
	pyplot.hold(False)

	return saveFigure(title,show)

def scatter3(xAxis,yAxis,zAxis,title="",xLabel="x",yLabel="y",zLabel="z",show=False):
	"method to plot the class data and if DEBUG = False save the figure"

	matplotlib.rcParams['legend.fontsize'] = 10

	figure = pyplot.figure(num=title)
	axes = Axes3D(figure)
	
	axes.scatter(xAxis, yAxis, zAxis, label=title)
	axes.set_xlabel(xLabel,fontsize=FONTSIZE)
	axes.set_ylabel(yLabel,fontsize=FONTSIZE)
	axes.set_zlabel(zLabel,fontsize=FONTSIZE)
	axes.set_title(title,fontsize=FONTSIZE)
	axes.legend(fontsize=FONTSIZE)

	return saveFigure(title,show)

if (__name__ == "__main__"):

	pyplot.close("all")

	histogram([2,4,5,6.7])
	histogram(numpy.random.randn(2000)*8)
	histogram(numpy.random.randn(2000)*8,lines=[2,3],show=True)

	scatter([0,1,2],[0,1,2])
	scatter3([0,1,2,8],[0,1,2,3],[0,1,2,4])
	scatter("hello",{"point1":(1,2),"point2":(1,4),"   ":(2,4)})