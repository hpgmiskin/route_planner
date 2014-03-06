#Code to compile the report
from shared import *
from texDocument import TexDocument
import travellingPlane,dubinPath,plot,time

Report = TexDocument("Report.tex")
hypercubesConsidered = [10,25,50,100]
sectionRefs={"intro":"","plane":"","energy":"","latin":"","route":"","exact":"","improve":"","progressive":"","path":""}
planeData = {"Wingspan":3,"Turn Radius":0.1}

def introduction():
	"function to compile the report intoduction"

	title = "Gathering Atmospheric Data"
	subtitle = "Using an Unmanned Air Vehicle"
	abstract = "This report looks at three dimensional energy based path planning for unmanned air vehicles in a predetermined area, with particular consideration to quality of data produced."
	Report.titlePage(title,subtitle,abstract)

	sectionRefs["intro"] = Report.section("Introduction")
	Report.paragraph("The following section outline the process in which a minimum cost route through a sample space can be obtained that provides the best data collection quality")

	sectionRefs["plane"] = Report.section("Plane Properties")
	planeTable = [[key,value] for key,value in planeData.items()]
	planeTableRef = Report.table("Table of Plane Properties",planeTable)
	Report.paragraph("To considere th minimum cost of circumnavigating a particular route the specifications of a plane must be considered in table {} the plane detailed in this table is the plane that is used for the entire report".format(planeTableRef))
	alpha,beta = 10,6

	sectionRefs["energy"] = Report.section("Energy Model")
	energyEquationRef = Report.equation("Energy Equation",r"E=\alpha D + \beta H")
	Report.paragraph(r"From these plane properties the following energy model has been definened in equation {} where $\alpha$ and $\beta$ are coeficients that are determined by the plane. For the current plane shown in table {} $\alpha$ and $\beta$ take values of {} and {} respectively.".format(energyEquationRef,planeTableRef,alpha,beta))

	sectionRefs["latin"] = Report.section("Latin Hypercubes")
	Report.paragraph("Latin hypercubes are sampling pland that provide the best space fillingness while limiting the total number of sampling points required. This is generally applied to testing of computer similations where the collection of each point is expensive. In this situation however the travel bertween the points the expensive component.")

	numberOfPoints = hypercubesConsidered
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

def exactPlanning():
	"function to compile the report path planning component"

	sectionRefs["route"] = Report.section("Route Planning")
	Report.paragraph("Given a set of points within a sample space the next stage of the proceedings is to compute the least cost route through these points. This problem presents itself in the forn of the travelling salesman problem. The travelling salesman problem is the problem of finding the least cost route through a set of points. There is lots of work done on the elicidean travelling salesman problem and introducing heroustics to improe the time taken to compute. This is due to the problem being an NP hard problem (the computing time required increases exponentially with the number of points in the route)")

	sectionRefs["exact"] = Report.section("Exact Travelling Salesman","sub")

	numberOfPoints = [4,6,8,10]
	captions = []
	filenames = []
	exactResults = {"numberOfPoints":numberOfPoints,"numberOfRoutes":[],"computeTime":[],"bestCost":[]}
	for numberOfPoint in numberOfPoints:
		#load latin hypercube of given nodes
		nodes = latinHypercube(numberOfPoint)
		#time how long it takes to calculate all routes
		tic = time.time()
		routes,costs = travellingPlane.allRoutes(nodes)
		toc= time.time()
		exactResults["numberOfRoutes"].append(len(routes))
		computeTime = round(toc-tic,3)*1000
		exactResults["computeTime"].append(computeTime)
		#compute best cost
		bestCost = min(costs)
		exactResults["bestCost"].append(round(bestCost,2))
		#compute best route and obtain ordered nodes
		bestRoute = routes[costs.index(bestCost)]
		orderedNodes = travellingPlane.orderNodes(nodes,bestRoute)
		[x,y,z] = changeArray(orderedNodes)
		#plot the resulting route
		captions.append("{} Nodes".format(numberOfPoint))
		filename = plot.line3(x,y,z,"Exact TSP of {} Nodes".format(numberOfPoint))
		filenames.append(filename)

	#clear old memory
	routes = None

	caption = "Exact routes calculated by travelling salesman"
	exactFigureRef,exactFigureRefs = Report.figures(caption,captions,filenames)
	Report.paragraph("Figure {} shows the optimal routes for differnt numbers of nodes. These optimal routes are found by computing the exact cost of each and every route option. Although this yield the shortest routes this approach is not efficient in terms of the computation time required.".format(exactFigureRef))

	exactTableRef = Report.table("Comparison of route calculation",[
		["Number of points"]+exactResults["numberOfPoints"],
		["Number of possible routes"]+exactResults["numberOfRoutes"],
		["Computation time (ms)"]+exactResults["computeTime"],
		["Best route cost (J)"]+exactResults["bestCost"]
		],"l")

	Report.paragraph("Table {} shows the number of possible routes and the resulting computation time given different numbers of nodes. It can easily be seen that the number of route options is equivilent to $n!$ where $n$ is the number of nodes. The number of routes directly realtes to the computation time.".format(exactTableRef))
	Report.paragraph("The computation time of the exact TSP approach can be reduced in a number of ways. Primarily the start node of the calculation can be defined however this only reduces the complexity to the equivilent of removoing a node form the computation. Other approaches involve producing a best guess and improving upon that. The approach taken in this project is taken from considering the best routes in figure {} generally comprise of a climbing component and a decending component.".format(exactFigureRef))

	sectionRefs["improve"] = Report.section("Improving Travelling Salesman","sub")
	Report.paragraph("The progressive travelling salesman is an approach to computing a best guess route for the least energy route for a number of points. The computation process is as follows")
	Report.list([
		"Order the nodes by there vertical location from lowest to highest",
		"Considering the lowest N nodes compute all posible combinations to produce two routes from the given nodes",
		"Compare all permutations of routes to return the least cost combination",
		"Add first nodes of both routes to final route",
		"Consider lowest N nodes that are not in the final route and reitterate",
		"Work through all nodes until no nodes are left without a route"
		],"enumerate")

	nodesPerRoutes = [2,3,4,5]
	solutionLines = {}
	progressiveResults = {"nodesPerRoutes":nodesPerRoutes,"computeTime":[],"bestRoute":[],"bestCost":[]}
	#load latin hypercube of required nodes
	nodes = latinHypercube(numberOfPoint)
	for nodesPerRoute in nodesPerRoutes:
		#time how long it takes to calculate route
		tic = time.time()
		bestRoute,bestCost = travellingPlane.progressiveRoute(nodes,nodesPerRoute)
		toc = time.time()
		#save computation time
		progressiveResults["computeTime"].append(round(toc-tic,3)*1000)
		#save best route and cost
		progressiveResults["bestRoute"].append(bestRoute)
		progressiveResults["bestCost"].append(round(bestCost,2))
		#save the best solutions as lines
		solutionLines["{} Nodes".format(nodesPerRoute)]=bestCost
		
	progressiveTableRef = Report.table("Comparison of route calculation",[
		["Nodes in each route"]+progressiveResults["nodesPerRoutes"],
		["Computation time (ms)"]+progressiveResults["computeTime"],
		["Best route cost (J)"]+progressiveResults["bestCost"]
		],"l")
	Report.paragraph("Table {} shows the varying computation time for routes through a {} node latin hypercube that have a differnet numbers of nodes in each route. This refers to the number of nodes that are consideered in each progressive itteration of the code.".format(progressiveTableRef,numberOfPoint))

	title = "Histogram of {} node route costs".format(numberOfPoint)
	filename = plot.histogram(costs,title,"Cost","Frequency",solutionLines)
	histRef = Report.figure(filename,title)
	Report.paragraph("Figure {} shows a histogram of differnt route costs for a {} node latin hypercube. The lines on this histogram plot represent the best cost routes with different numbers of nodes in the route".format(histRef,numberOfPoint))

def progressivePlanning():
	"function to compile report on progressive path planning"

	sectionRefs["progressive"] = Report.section("Progressive Travelling Salesman","sub")
	nodesPerRoute = 4
	Report.paragraph("In section {} a best guess approach to the travelling salesman was presented and compared with the exact results. Given the results were close to the optimum even when the progressive algorithem only considered 2 nodes in the route it can be brought forward to be considered in reference to larger route problems. In these routes {} nodes are considered for both the up route and the down route are used at each stage of the progressive algorithm.".format(sectionRefs["progressive"],nodesPerRoute))

	numberOfPoints = hypercubesConsidered
	captions = []
	filenames = []
	progressiveResults = {"numberOfPoints":numberOfPoints,"computeTime":[],"bestCost":[]}
	for numberOfPoint in numberOfPoints:
		#load latin hypercube of given nodes
		nodes = latinHypercube(numberOfPoint)
		#time how long it takes to calculate all routes
		tic = time.time()
		bestRoute,bestCost = travellingPlane.progressiveRoute(nodes,nodesPerRoute)
		toc= time.time()
		#populatee results
		computeTime = round(toc-tic,3)*1000
		progressiveResults["computeTime"].append(computeTime)
		progressiveResults["bestCost"].append(round(bestCost,2))
		#obtain ordered nodes from best route
		orderedNodes = travellingPlane.orderNodes(nodes,bestRoute)
		[x,y,z] = changeArray(orderedNodes)
		#plot the resulting route
		captions.append("{} Nodes".format(numberOfPoint))
		filename = plot.line3(x,y,z,"Progressive TSP of {} Nodes".format(numberOfPoint))
		filenames.append(filename)

	caption = "Exact routes calculated by travelling salesman"
	progressiveFigureRef,progressiveFigureRefs = Report.figures(caption,captions,filenames)
	Report.paragraph("Figure {} shows a number of optimal routes for varing numbers of nodes whos order is defined be the progressive travelling salesman algorithm. Though the {} node route is difficult to see the exact routing the other routes show a logical approach to the routing problem".format(progressiveFigureRef,numberOfPoint))

	progressiveTableRef = Report.table("Comparison of progressive route calculation",[
		["Number of points"]+progressiveResults["numberOfPoints"],
		["Computation time (ms)"]+progressiveResults["computeTime"],
		["Best route cost (J)"]+progressiveResults["bestCost"]
		],"l")
	Report.paragraph("Table {} shows the computation time and route cost for the differnt routing situations. The computation time is far bellow that of the exact travelling salesman algorithm due to the complexity of this problem being broken down into {} node chunks".format(progressiveTableRef,nodesPerRoute))

def pathPlanning():
	"function to compile the path planning component of the report"

	sectionRefs["path"] = Report.section("Path Planning")
	Report.paragraph("The least energy route through a number of nodes has been defined however this route assumes that the UAV is able to turn on the spot and is not constricted by turning radius. Therefore to compute the actual energy cost of circumnavigating a route the turning radius of the UAV needs to be considered. Dubins paths are the minimum distance paths given a start and end direction.")
	Report.paragraph("Duibins paths ar comprised of maximum rate turns and straight line segments. The following defines all the routes that are possible made op of maxiumum rate turns and straight line segments")
	Report.list([
		"RSR - Right Turn, Straight Flight then Right Turn",
		"RSL - Right Turn, Straight Flight then Left Turn",
		"LSR - Left Turn, Straight Flight then Right Turn",
		"LSL - Left Turn, Straight Flight then Left Turn",
		"RLR - Right Turn, Left Turn then Right Turn",
		"LRL - Left Turn, Right Turn then Left Turn",
		])


	nodesPerRoute = 4
	numberOfPoint = 10
	nodes = latinHypercube(numberOfPoint)
	bestRoute,bestCost = travellingPlane.progressiveRoute(nodes,nodesPerRoute)
	orderedNodes = travellingPlane.orderNodes(nodes,bestRoute)
	x,y,z = changeArray(orderedNodes)

	plot.line3(x,y,z,show=True)

	currentPath = dubinPath.DubinPath(planeData["Turn Radius"])

	for node in orderedNodes:
		currentPath.addNode(node)

	currentPath.plotPath()

if __name__ == "__main__":
	introduction()
	# exactPlanning()
	# progressivePlanning()
	pathPlanning()
