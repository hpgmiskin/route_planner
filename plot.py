import numpy,matplotlib,itertools
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot
from shared import naturalKeys

FONTSIZE = 10

def saveFigure(title,show):
	"function to save or show the current figure given the title"

	pyplot.autoscale(enable=True, axis='both', tight=True)

	if show:
		pyplot.show()
		pyplot.close()
		return None
	else:
		filename = "figures/{}.png".format(title.replace(" ","_").lower())
		pyplot.savefig("report/"+filename)
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
		for name,line in sorted(lines.items(),key=lambda x:naturalKeys(x[0]),reverse=True):
			pyplot.plot([line,line],[0,maxFrequency],label=name,linewidth=1)
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

def line(xAxis,yAxis,title="",xLabel="x",yLabel="y",xTicks=None,yTicks=None,show=False):
	"method to plot the class data and if DEBUG = False save the figure"

	pyplot.figure(num=title)
	pyplot.hold(True)
	pyplot.title(title)

	if (type(xAxis[0]) == str):
		xTicks = xAxis
		xAxis = numpy.arange(len(xAxis))

	if (type(yAxis) == dict):
		yMin,yMax = 0,0
		for name,data in sorted(yAxis.items(),key=lambda x:naturalKeys(x[0])):
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
	# axes.set_aspect('equal')

	axes.plot(xAxis, yAxis, zAxis, label=title)
	#scaleBox(axes,xAxis, yAxis, zAxis)
	
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
	#axes.set_aspect('equal')

	for label,data in paths.items():
		[x,y,z] = data
		axes.plot(x, y, z, label=label)

	#scaleBox(axes,x, y, z)

	pyplot.hold(False)
	axes.set_xlabel(xLabel,fontsize=FONTSIZE)
	axes.set_ylabel(yLabel,fontsize=FONTSIZE)
	axes.set_zlabel(zLabel,fontsize=FONTSIZE)
	axes.set_title(title,fontsize=FONTSIZE)
	axes.legend()

	return saveFigure(title,show)

def scatter(xAxis,yAxis,title="",xLabel="x",yLabel="y",xTicks=None,yTicks=None,lines=None,show=False):
	"method to plot the class data and if DEBUG = False save the figure"

	pyplot.figure(num=title)
	axes = pyplot.axes()
	pyplot.hold(True)
	pyplot.title(title,fontsize=FONTSIZE)

	maxValue = 0
	minValue = numpy.infty

	if (type(xAxis[0]) == str):
		xTicks = xAxis
		xAxis = numpy.arange(len(xAxis))

	if (type(yAxis) == dict):
		colours = itertools.cycle(["b","g","r","c","m","y","k"])
		for name,data in sorted(yAxis.items(),key=lambda x:naturalKeys(x[0])):
			minValue = min(data+[minValue])
			maxValue = max(data+[maxValue])
			axes.scatter(xAxis[:len(data)],data[:len(xAxis)],label=name,color=next(colours))
	elif (type(yAxis) == list):
		axes.scatter(xAxis[:len(yAxis)],yAxis[:len(xAxis)],label="")
	else:
		raise ValueError("Plot expected list or dictionary for yAxis")

	if xTicks:
		axes.xticks(xAxis, xTicks, rotation=0)

	axes.set_xlabel(xLabel,fontsize=FONTSIZE)
	axes.set_ylabel(yLabel,fontsize=FONTSIZE)
	axes.set_title(title,fontsize=FONTSIZE)
	handles, labels = axes.get_legend_handles_labels()
	l1 = axes.legend(handles,labels,loc=4,fontsize=FONTSIZE)

	if lines:
		for name,line in sorted(lines.items(),key=lambda x:naturalKeys(x[0])):
			axes.plot(line[0],line[1],label=name,linewidth=1)
		handles2, labels2 = axes.get_legend_handles_labels()

		for i in range(len(handles)):
			handles2.remove(handles[i])
			labels2.remove(labels[i])

		l2 = axes.legend(handles2,labels2,loc=2,fontsize=FONTSIZE)
		pyplot.gca().add_artist(l1)

	pyplot.hold(False)

	return saveFigure(title,show)

def scatter3(xAxis,yAxis,zAxis,title="",xLabel="x",yLabel="y",zLabel="z",show=False):
	"method to plot the class data and if DEBUG = False save the figure"

	matplotlib.rcParams['legend.fontsize'] = FONTSIZE

	figure = pyplot.figure(num=title)
	axes = Axes3D(figure)
	#axes.set_aspect('equal')
	
	axes.scatter(xAxis, yAxis, zAxis, label=title)
	#scaleBox(axes,xAxis, yAxis, zAxis)

	axes.set_xlabel(xLabel,fontsize=FONTSIZE)
	axes.set_ylabel(yLabel,fontsize=FONTSIZE)
	axes.set_zlabel(zLabel,fontsize=FONTSIZE)
	axes.set_title(title,fontsize=FONTSIZE)
	axes.legend(fontsize=FONTSIZE)

	return saveFigure(title,show)

def scaleBox(axes,xAxis,yAxis,zAxis):
	"plots a invisible scale box to correct the aspect ratio"

	pyplot.hold(True)

	# Create cubic bounding box to simulate equal aspect ratio
	max_range = numpy.array([max(xAxis)-min(xAxis), max(yAxis)-min(yAxis), max(zAxis)-min(zAxis)]).max()
	Xb = 0.5*max_range*numpy.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(max(xAxis)+min(xAxis))
	Yb = 0.5*max_range*numpy.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(max(yAxis)+min(yAxis))
	Zb = 0.5*max_range*numpy.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(max(zAxis)+min(zAxis))
	# Comment or uncomment following both lines to test the fake bounding box:
	for xb, yb, zb in zip(Xb, Yb, Zb):
	   axes.plot([xb], [yb], [zb], 'w')

	pyplot.hold(False)

if (__name__ == "__main__"):

	pyplot.close("all")

	histogram([2,4,5,6.7])
	histogram(numpy.random.randn(2000)*8)
	histogram(numpy.random.randn(2000)*8,lines=[2,3],show=True)

	scatter([0,1,2],[0,1,2])
	scatter3([0,1,2,8],[0,1,2,3],[0,1,2,4])
	scatter("hello",{"point1":(1,2),"point2":(1,4),"   ":(2,4)})