import numpy,matplotlib
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot

FONTSIZE = 10

def plotHistogram(data,numberBars=10,title="",xLabel="",yLabel="",show=False):
	"plots a histogram of the given data data"

	pyplot.figure()
	pyplot.hist(data,numberBars)
	pyplot.title(title,fontsize=FONTSIZE)
	pyplot.xlabel(xLabel,fontsize=FONTSIZE)
	pyplot.ylabel(yLabel,fontsize=FONTSIZE)

	if show:
		pyplot.show()
		pyplot.close()
	else:
		pyplot.savefig(title)

def plotBar(labels,values,title="",xLabel="",yLabel="",show=False):
	"plots a bar chart with the givne labels and data values"

	length = len(values)

	indexs = numpy.arange(length)
	barWidth = 1

	figure = pyplot.figure()
	axes = pyplot.axes()

	barAxes = pyplot.bar(indexs,values,barWidth)

	pyplot.legend(barAxes,labels,fontsize=FONTSIZE)
	pyplot.title(title,fontsize=FONTSIZE)

	labels = [label[:10] for label in labels]
	pyplot.xticks(indexs + barWidth/2, labels, rotation=0)
	pyplot.yticks(range(0,max(values)+10,5))
	
	pyplot.xlabel(xLabel,fontsize=FONTSIZE)
	pyplot.ylabel(yLabel,fontsize=FONTSIZE)

	if show:
		pyplot.show()
		pyplot.close()
	else:
		pyplot.savefig(title)
False
def plotPie(labels,values,title="",xLabel="",yLabel="",show=False):
	"plot a pie cahrt with the given labels and data values"

	figure = pyplot.figure(num=title)
	axes = pyplot.axes()

	pyplot.pie(values, labels=[label[:10] for label in labels])
	pyplot.legend(labels,fontsize=FONTSIZE)
	pyplot.title(title,fontsize=FONTSIZE)

	pyplot.xlabel(xLabel,fontsize=FONTSIZE)
	pyplot.ylabel(yLabel,fontsize=FONTSIZE)

	if show:
		pyplot.show()
		pyplot.close()
	else:
		pyplot.savefig(title)

def plotLine(xAxis,yAxis,title="",xLabel="",yLabel="",xTicks=None,yTicks=None,show=False):
	"method to plot the class data and if DEBUG = False save the figure"

	pyplot.figure(num=title)
	pyplot.hold(True)
	pyplot.title(title)

	if (type(xAxis[0]) == str):
		xTicks = xAxis
		xAxis = numpy.arange(len(xAxis))

	if (type(yAxis) == dict):
		for name,data in sorted(yAxis.items(),key=lambda x:x[0]):
			pyplot.plot(xAxis[:len(data)],data[:len(xAxis)],label=name)
	elif (type(yAxis) == list):
		pyplot.plot(xAxis[:len(yAxis)],yAxis[:len(xAxis)],label="")
	else:
		raise ValueError("Plot expected list or dictionary for yAxis")

	if xTicks:
		pyplot.xticks(xAxis, xTicks, rotation=0)

	pyplot.xlabel(xLabel,fontsize=FONTSIZE)
	pyplot.ylabel(yLabel,fontsize=FONTSIZE)
	pyplot.legend(fontsize=FONTSIZE)
	pyplot.hold(False)

	if show:
		pyplot.show()
	else:
		pyplot.savefig(title)

def plotLine3(xAxis,yAxis,zAxis,title="",xLabel="",yLabel="",zLabel="",show=False):
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

    if show:
        figure.show()
    else:
        figure.savefig(title)

def plotScatter(xAxis,yAxis,title="",xLabel="",yLabel="",xTicks=None,yTicks=None,show=False):
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

	if show:
		pyplot.show()
	else:
		pyplot.savefig(title)

def plotScatter3(xAxis,yAxis,zAxis,title="",xLabel="",yLabel="",zLabel="",show=False):
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

    if show:
        pyplot.show()
    else:
        pyplot.savefig(title)

if (__name__ == "__main__"):

	pyplot.close("all")

	plotHistogram([2,4,5,6.7])
	plotHistogram(numpy.random.randn(2000)*8)

	plotScatter([0,1,2],[0,1,2])
	plotScatter3([0,1,2,8],[0,1,2,3],[0,1,2,4])
	plotScatter("hello",{"point1":(1,2),"point2":(1,4),"   ":(2,4)})