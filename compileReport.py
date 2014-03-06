#Code to compile the report
from shared import *
from texDocument import TexDocument
import travellingPlane,dubinPath,plot,time

Report = TexDocument("Report.tex")

title = "Gathering Atmospheric Data"
subtitle = "Using an Unmanned Air Vehicle"
abstract = "This report looks at three dimensional energy based path planning for unmanned air vehicles in a predetermined area, with particular consideration to quality of data produced."
Report.titlePage(title,subtitle,abstract)

introRef = Report.section("Introduction")
Report.paragraph("The following section outline the process in which a minimum cost route through a sample space can be obtained that provides the best data collection quality")

planeRef = Report.section("Plane Properties")
planeTableRef = Report.table("Table of Plane Properties",[["Name","Wingspan","height"],["Plane 1","20m","5m"],["Plane 3","40m","6m"]])
Report.paragraph("To considere th minimum cost of circumnavigating a particular route the specifications of a plane must be considered in table {} the properties of differnt planes is shown".format(planeTableRef))
alpha,beta = 10,6

energyRef = Report.section("Energy Model")
energyEquationRef = Report.equation("Energy Equation",r"E=\alpha D + \beta H")
Report.paragraph(r"From these plane properties the following energy model has been definened in equation {} where $\alpha$ and $\beta$ are coeficients that are determined by the plane. For the current plane shown in table {} $\alpha$ and $\beta$ take values of {} and {} respectively.".format(energyEquationRef,planeTableRef,alpha,beta))

latinRef = Report.section("Latin Hypercubes")
Report.paragraph("Latin hypercubes are sampling pland that provide the best space fillingness while limiting the total number of sampling points required. This is generally applied to testing of computer similations where the collection of each point is expensive. In this situation however the travel bertween the points the expensive component.")

numberOfPoints = [10,50,250,1250]
captions = []
filenames = []
for numberOfPoint in numberOfPoints:
	nodes = latinHypercube(numberOfPoint)
	[x,y,z] = changeArray(nodes)
	filename = plot.scatter3(x,y,z,"Nodes {}".format(numberOfPoint))
	filenames.append(filename)
	captions.append("{} Nodes".format(numberOfPoint))
caption = "Latin Hypercubes with Varying Numbers of Nodes"
latinFigureRef,LatinFigureRefs = Report.figures(caption,captions,filenames)

Report.paragraph("Figure {} shows a number of latin hypercubes with differnt numbers of nodes. All the Latin Hypercubes are within a unit cube. For collection of data in a required area these cubes can be stretched to fill the desired space. This does not provide an even spacing in each direction however means that eeach vertex of data collection is equally considered.".format(latinFigureRef))
Report.paragraph("For this project the idea is to follow this logic to utilise Latin Hypercubes:")
Report.list([
	"Specifiy area of interest to researcher",
	"Estimate number of nodes able to be circumnavigated given the UAV total energy and the area of sample space",
	"Fit Latin Hypercube of given nodes to sample area",
	"Calcualte least energy route through the sample space",
	"After first flight asses areas of encertainty to plan route through for next flight"
	],"enumerate")

pathRef = Report.section("Path Planning")
Report.paragraph("Given a set of points within a sample space the next stage of the proceedings is to compute the least cost path through these points. This problem presents itself in the forn of the travelling salesman problem. The travelling salesman problem is the problem of finding the least cost path through a set of points. There is lots of work done on the elicidean travelling salesman problem and introducing heroustics to improe the time taken to compute. This is due to the problem being an NP hard problem (the computing time required increases exponentially with the number of points in the route)")

numberOfPoints = [4,6,8,10]
captions = []
filenames = []
results = {"numberOfPoints":numberOfPoints,"numberOfRoutes":[],"computeTime":[],"bestCost":[]}
for numberOfPoint in numberOfPoints:
	#load latin hypercube of given nodes
	nodes = latinHypercube(numberOfPoint)
	#time how long it takes to calculate all routes
	tic = time.time()
	routes,costs = travellingPlane.allRoutes(nodes)
	toc= time.time()
	results["numberOfRoutes"].append(len(routes))
	results["computeTime"].append(round(toc-tic,4)*1000)
	#compute best and worst costs
	bestCost = min(costs)
	worstCost = max(costs)
	results["bestCost"].append(round(bestCost,2))
	#compute best route and obtain ordered nodes
	bestRoute = routes[costs.index(bestCost)]
	orderedNodes = travellingPlane.orderNodes(nodes,bestRoute)
	[x,y,z] = changeArray(orderedNodes)
	#plot the resulting route
	captions.append("{} Nodes".format(numberOfPoint))
	filename = plot.line3(x,y,z,"Exact TSP of {} Nodes".format(numberOfPoint))
	filenames.append(filename)

caption = "Exact routes calculated by travelling salesman"
exactFigureRef,exactFigureRefs = Report.figures(caption,captions,filenames)
Report.paragraph("Figure {} shows the optimal routes for differnt numbers of nodes. These optimal routes are found by computing the exact cost of each and every route option. Although this yield the shortest routes this approach is not efficient in terms of the computation time required.".format(exactFigureRef))

exactTableRef = Report.table("Comparison of route calculation",[
	["Number of points"]+results["numberOfPoints"],
	["Number of possible routes"]+results["numberOfRoutes"],
	["Computation time (ms)"]+results["computeTime"]#,
	#["Best route cost (J)"]+results["bestCost"]
	],"l")

Report.paragraph("Table {} shows the number of possible routes and the resulting computation time given different numbers of nodes. It can easily be seen that the number of route options is equivilent to $n!$ where $n$ is the number of nodes. The number of routes directly realtes to the computation time.".format(exactTableRef))
Report.paragraph("")

title = "Histogram of {} node route costs".format(numberOfPoints[-1])
filename = plot.histogram(costs,title)
histRef = Report.figure(filename,title)
Report.paragraph("Figure {} shows a histogram of differnt route costs for a {} node latin hypercube".format(histRef,numberOfPoints[-1]))