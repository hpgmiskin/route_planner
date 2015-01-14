import re,numpy,matplotlib,itertools
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot
from shared import naturalKeys

FONTSIZE = 16

def saveFigure(title,show=False,tight=True):
	"function to save or show the current figure given the title"

	pyplot.autoscale(enable=True, axis='both', tight=tight)

	if show:
		pyplot.show()
		pyplot.close()
		return None
	else:
		title =  re.subn(r"[\s$]","_",title)[0]
		title =  re.subn(r"[^\w\d_]","",title)[0]
		filename = "figures/{}.png".format(title.lower())
		pyplot.savefig("report/"+filename)
		pyplot.close("all")
		return filename

def histogram(data,title="",xLabel="Value",yLabel="Frequency",lines=None,numberBars=10,show=False):
	"plots a histogram of the given data data"

	maxFrequency = len(data)/numberBars

	pyplot.figure(num=title)
	pyplot.hold(True)
	pyplot.hist(data,numberBars)
	#pyplot.title(title,fontsize=FONTSIZE)
	pyplot.xlabel(xLabel,fontsize=FONTSIZE)
	pyplot.ylabel(yLabel,fontsize=FONTSIZE)

	if lines:
		for name,line in sorted(lines.items(),key=lambda x:naturalKeys(x[0]),reverse=True):
			pyplot.plot([line,line],[0,maxFrequency],label=name,linewidth=1)
		pyplot.legend()

	pyplot.hold(False)

	return saveFigure(title,show)

def bar(labels,values,title="",xLabel="",yLabel="",lines=False,show=False):
	"plots a bar chart with the givne labels and data values"

	def plot9():
	    data = [ ("data1", 34), ("data2", 22),
	            ("data3", 11), ( "data4", 28),
	            ("data5", 57), ( "data6", 39),
	            ("data7", 23), ( "data8", 98)]
	    N = len( data )
	    x = np.arange(1, N+1)
	    y = [ num for (s, num) in data ]
	    labels = [ s for (s, num) in data ]
	    width = 1
	    bar1 = plt.bar( x, y, width, color="y" )
	    plt.ylabel( 'Intensity' )
	    plt.xticks(x + width/2.0, labels )
	    plt.show()

	length = len(values)

	indexs = numpy.arange(length)
	barWidth = 1

	figure = pyplot.figure(num=title)
	axes = pyplot.axes()

	pyplot.hold(True)
	barAxes = pyplot.bar(indexs,values,barWidth)

	pyplot.legend(barAxes,labels,fontsize=FONTSIZE)
	#pyplot.title(title,fontsize=FONTSIZE)

	labels = [label[:10] for label in labels]
	pyplot.xticks(indexs + barWidth/2, labels, rotation=0)
	pyplot.yticks(range(0,max(values)+10,5))
	
	pyplot.xlabel(xLabel,fontsize=FONTSIZE)
	pyplot.ylabel(yLabel,fontsize=FONTSIZE)

	if lines:
		for name,line in sorted(lines.items(),key=lambda x:naturalKeys(x[0]),reverse=True):
			pyplot.plot([line,line],[0,maxFrequency],label=name,linewidth=1)
		pyplot.legend()

	pyplot.hold(False)

	return saveFigure(title,show)

def pie(labels,values,title="",xLabel="",yLabel="",show=False):
	"plot a pie cahrt with the given labels and data values"

	figure = pyplot.figure(num=title)
	axes = pyplot.axes()

	pyplot.pie(values, labels=[label[:10] for label in labels])
	pyplot.legend(labels,fontsize=FONTSIZE)
	#pyplot.title(title,fontsize=FONTSIZE)

	pyplot.xlabel(xLabel,fontsize=FONTSIZE)
	pyplot.ylabel(yLabel,fontsize=FONTSIZE)

	return saveFigure(title,show)

def line(xAxis,yAxis,title="",xLabel="x",yLabel="y",location=4,scatter=None,xTicks=None,yTicks=None,tight=True,show=False):
	"method to plot the class data and if DEBUG = False save the figure"

	pyplot.figure(num=title)
	pyplot.hold(True)
	#pyplot.title(title)

	if (type(xAxis[0]) == str):
		xTicks = xAxis
		xAxis = numpy.arange(len(xAxis))

	if (type(yAxis) == dict):
		yMin,yMax = 0,0
		for name,data in sorted(yAxis.items(),key=lambda x:naturalKeys(x[0])):
			yMin = min(data+[yMin])
			yMax = max(data+[yMax])
			pyplot.plot(xAxis[:len(data)],data[:len(xAxis)],label=name)
		pyplot.legend(fontsize=FONTSIZE,loc=location)
	else:
		yMin = min(yAxis)
		yMax = max(yAxis)
		pyplot.plot(xAxis[:len(yAxis)],yAxis[:len(xAxis)],label="")

	if xTicks:
		pyplot.xticks(xAxis, xTicks, rotation=0)

	if scatter:
		for name,data in scatter.items():
			pyplot.scatter(data[0],data[1],label=name)

	pyplot.xlabel(xLabel,fontsize=FONTSIZE)
	pyplot.ylabel(yLabel,fontsize=FONTSIZE)
	ySpace = (yMax-yMin)*0.05
	pyplot.ylim((yMin-ySpace,yMax+ySpace))
	pyplot.hold(False)

	return saveFigure(title,show,tight)

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
	#axes.set_title(title,fontsize=FONTSIZE)
	axes.legend()

	return saveFigure(title,show)

def path(paths,title="",xLabel="x",yLabel="y",arrows=None,show=False,tight=True):
	"function to plot the given paths"

	figure = pyplot.figure(num=title)
	axes = pyplot.axes()
	pyplot.hold(True)
	#pyplot.title(title)

	for label,data in sorted(paths.items(),key=lambda x:naturalKeys(x[0])):
		if len(data) == 3:
			[x,y,z] = data
		else:
			[x,y] = data
		axes.plot(x[:len(y)],y[:len(x)],label=label)

	if arrows:
		for label,data in arrows.items():
			[x1,y1,x2,y2] = data
			axes.arrow(x1,y1,x2,y2,head_width=0.1, fc='k', ec='k')

	axes.set_xlabel(xLabel,fontsize=FONTSIZE)
	axes.set_ylabel(yLabel,fontsize=FONTSIZE)
	#axes.set_title(title,fontsize=FONTSIZE)
	axes.legend(loc=4)
	pyplot.hold(False)
	pyplot.axis('equal')

	return saveFigure(title,show,tight)

def path2(paths,title="",xLabel="x",yLabel="y",scatter=None,show=False):
	"function to plot the given paths"

	figure = pyplot.figure(num=title)
	axes = pyplot.axes()
	pyplot.hold(True)
	#pyplot.title(title)

	for label,data in sorted(paths.items(),key=lambda x:naturalKeys(x[0])):
		[x,y] = data
		axes.plot(x[:len(y)],y[:len(x)],label=label)

	if scatter:
		for name,data in sorted(scatter.items(),key=lambda x:naturalKeys(x[0])):
			pyplot.scatter(data[0],data[1],label=name)

	axes.set_xlabel(xLabel,fontsize=FONTSIZE)
	axes.set_ylabel(yLabel,fontsize=FONTSIZE)
	#axes.set_title(title,fontsize=FONTSIZE)
	axes.legend(loc=4)
	pyplot.hold(False)

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
	#axes.set_title(title,fontsize=FONTSIZE)
	axes.legend()

	return saveFigure(title,show)

def scatter(xAxis,yAxis,title="",xLabel="x",yLabel="y",xTicks=None,yTicks=None,lines=None,show=False):
	"method to plot the class data and if DEBUG = False save the figure"

	pyplot.figure(num=title)
	axes = pyplot.axes()
	pyplot.hold(True)
	#pyplot.title(title,fontsize=FONTSIZE)

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
		handles, labels = axes.get_legend_handles_labels()
		l1 = axes.legend(handles,labels,loc=4,fontsize=FONTSIZE)
	else:
		axes.scatter(xAxis[:len(yAxis)],yAxis[:len(xAxis)],label="")

	if xTicks:
		axes.xticks(xAxis, xTicks, rotation=0)

	axes.set_xlabel(xLabel,fontsize=FONTSIZE)
	axes.set_ylabel(yLabel,fontsize=FONTSIZE)
	#axes.set_title(title,fontsize=FONTSIZE)

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

def scatter2(series,title="",xLabel="x",yLabel="y",xTicks=None,yTicks=None,lines=None,location=4,show=False):
	"method to plot the class data and if DEBUG = False save the figure"

	pyplot.figure(num=title)
	axes = pyplot.axes()
	pyplot.hold(True)
	#pyplot.title(title,fontsize=FONTSIZE)

	colours = itertools.cycle(["b","g","r","c","m","y","k"])
	for name,data in sorted(series.items(),key=lambda x:naturalKeys(x[0])):
		axes.scatter(data[0],data[1],label=name,color=next(colours))

	for name,data in sorted(lines.items(),key=lambda x:naturalKeys(x[0])):
		axes.plot(data[0],data[1],label=name,color=next(colours))

	axes.set_xlabel(xLabel,fontsize=FONTSIZE)
	axes.set_ylabel(yLabel,fontsize=FONTSIZE)
	#axes.set_title(title,fontsize=FONTSIZE)
	axes.legend(fontsize=FONTSIZE,loc=location)

	pyplot.hold(False)

	return saveFigure(title,show)

def scatter3(xAxis,yAxis,zAxis,title="",xLabel="x",yLabel="y",zLabel="z",scaleBox=False,show=False):
	"function to plot a 3d scatter plot"

	matplotlib.rcParams['legend.fontsize'] = FONTSIZE
	figure = pyplot.figure(num=title)
	axes = Axes3D(figure)
	#axes.set_aspect('equal')
	
	if (type(zAxis) == dict):
		colours = itertools.cycle(["b","g","r","c","m","y","k"])
		for name,data in sorted(zAxis.items(),key=lambda x:naturalKeys(x[0])):
			axes.scatter(xAxis, yAxis, data, label=name, color=next(colours))
		axes.legend(fontsize=FONTSIZE)
	else:
		axes.scatter(xAxis, yAxis, zAxis, label=title)

	if scaleBox:
		addScaleBox(axes,xAxis, yAxis, zAxis)

	axes.set_xlabel(xLabel,fontsize=FONTSIZE)
	axes.set_ylabel(yLabel,fontsize=FONTSIZE)
	axes.set_zlabel(zLabel,fontsize=FONTSIZE)
	#axes.set_title(title,fontsize=FONTSIZE)

	return saveFigure(title,show)

def surface(xArray,yArray,zArray,title="",xLabel="x",yLabel="y",zLabel="z",show=False):
	"function to plot a surface plot"

	matplotlib.rcParams['legend.fontsize'] = FONTSIZE
	figure = pyplot.figure(num=title)
	axes = Axes3D(figure)

	axes.plot_surface(xArray,yArray,zArray)

	axes.set_xlabel(xLabel,fontsize=FONTSIZE)
	axes.set_ylabel(yLabel,fontsize=FONTSIZE)
	axes.set_zlabel(zLabel,fontsize=FONTSIZE)
	#axes.set_title(title,fontsize=FONTSIZE)

	return saveFigure(title,show)

def addScaleBox(axes,xAxis,yAxis,zAxis):
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