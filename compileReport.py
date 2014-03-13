#Code to compile the report
from shared import *
from texDocument import TexDocument
import latinHypercube,travellingPlane,dubinPath,plot,time

Report = TexDocument("report/Report.tex")
hypercubesConsidered = [10,25,50,100]
sectionRefs={"intro":"","plane":"","energy":"","latin":"","route":"","exact":"","improve":"","progressive":"","path":""}
planeData = {"Wingspan":3,"Turn Radius":0.1}

def introduction():
	"function to compile the report intoduction"

	print("introduction")

	title = "Gathering Atmospheric Data"
	subtitle = "Using an Unmanned Air Vehicle"
	abstract = "This report looks at three dimensional energy based path planning for unmanned air vehicles in a predetermined area, with particular consideration to quality of data produced."
	Report.titlePage(title,subtitle,abstract)

	sectionRefs["intro"] = Report.section("Introduction")
	Report.paragraph("The following section outlines the process in which a minimum cost route through a sample space can be obtained which provides the best data collection quality")

	Report.updateTex(open("report/aimsObjectives.tex").read())
	Report.updateTex(open("report/problemOutline.tex").read())
	Report.updateTex(open("report/lituratureReview.tex").read())

def method():
	"function to complile the report method"

	print("method")

	sectionRefs["plane"] = Report.section("Plane Properties")
	planeTable = [[key,"{}m".format(value)] for key,value in planeData.items()]
	planeTableRef = Report.table("Table of Plane Properties",planeTable)
	Report.paragraph("To considere th minimum cost of circumnavigating a particular route the specifications of a plane must be considered in table {} the plane detailed in this table is the plane that is used for the entire report".format(planeTableRef))
	alpha,beta = 10,6

	sectionRefs["energy"] = Report.section("Energy Model")
	energyEquationRef = Report.equation("Energy Equation",r"E=\alpha D + \beta H")
	Report.paragraph(r"From these plane properties the following energy model has been definened in equation {} where $\alpha$ and $\beta$ are coeficients that are determined by the plane. For the current plane shown in table {} $\alpha$ and $\beta$ take values of {} and {} respectively.".format(energyEquationRef,planeTableRef,alpha,beta))

	sectionRefs["latin"] = Report.section("Latin Hypercubes")
	Report.paragraph("Latin hypercubes are sampling plans that provide the best space fillingness while limiting the total number of sampling points required. This is generally applied to testing of computer similations where the collection of each point is expensive. In this situation however the travel bertween the points is the expensive component.")

	numberOfPoints = hypercubesConsidered
	captions = []
	filenames = []
	for numberOfPoint in numberOfPoints:
		nodes = latinHypercube.unitCube(numberOfPoint)
		[x,y,z] = changeArray(nodes)
		filename = plot.scatter3(x,y,z,"Nodes {}".format(numberOfPoint))
		filenames.append(filename)
		captions.append("{} Nodes".format(numberOfPoint))
	caption = "Latin Hypercubes with Varying Numbers of Nodes"
	latinFigureRef,LatinFigureRefs = Report.figures(filenames,caption,captions)

	Report.paragraph("Figure {} shows latin hypercubes with varying numbers of nodes. All the Latin Hypercubes are within a unit cube. For collection of data in a required area these cubes can be stretched to fill the desired space. This does not provide an even spacing in each direction however means that each vertex of data collection is equally considered in terms of spacing.".format(latinFigureRef))
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

	print("exactPlanning")

	sectionRefs["route"] = Report.section("Route Planning")
	Report.paragraph("Given a set of nodes within a sample space the next stage of the proceedings is to compute the least cost route through these nodes. This problem presents itself in the forn of the travelling salesman problem. The travelling salesman problem is the problem of finding the least cost route through a set of nodes. There is lots of work done on the elicidean travelling salesman problem and introducing heroustics to improve the time taken to compute. This is due to the problem being an NP hard problem (the computing time required increases exponentially with the number of nodes in the route)")

	sectionRefs["exact"] = Report.section("Exact Travelling Salesman","sub")

	numberOfPoints = [6,8,10,12]
	captions = []
	filenames = []
	exactResults = {"numberOfPoints":numberOfPoints,"numberOfRoutes":[],"computeTime":[],"bestCost":[]}
	for numberOfPoint in numberOfPoints:
		#load latin hypercube of given nodes
		nodes = latinHypercube.unitCube(numberOfPoint)
		#define start and end nodes
		sortedNodes = sorted(nodes,key=lambda x:x[2])
		startIndex = [i for i,node in enumerate(nodes) if all([node[j]==sortedNodes[0][j] for j in range(3)])][0]
		endIndex = [i for i,node in enumerate(nodes) if all([node[j]==sortedNodes[1][j] for j in range(3)])][0]
		#time how long it takes to calculate all routes
		tic = time.time()
		routes,costs = travellingPlane.allRoutes(nodes,startIndex,endIndex)
		toc= time.time()
		#compute best route and cost
		bestCost = min(costs)
		bestRoute = routes[costs.index(bestCost)]
		routes = None
		#save results
		exactResults["numberOfRoutes"].append(len(costs))
		exactResults["computeTime"].append(round(toc-tic,3)*1000)
		exactResults["bestCost"].append(round(bestCost,2))
		#obtain ordered nodes
		[x,y,z] = changeArray(travellingPlane.orderNodes(nodes,bestRoute,True))
		#plot the resulting route
		captions.append("{} Nodes".format(numberOfPoint))
		filename = plot.line3(x,y,z,"Exact TSP of {} Nodes".format(numberOfPoint))
		filenames.append(filename)

	caption = "Exact routes calculated by travelling salesman"
	exactFigureRef,exactFigureRefs = Report.figures(filenames,caption,captions)
	Report.paragraph("Figure {} shows the optimal routes for differnt numbers of nodes. These optimal routes are found by computing the exact cost of each and every route option. Although this yield the shortest routes this approach is not efficient in terms of the computation time required. To enable calculation of a {} node route the start and end points of the route is defiend by the two lowest nodes. This is due to the nature of a UAV flight commencing and finishing at ground level".format(exactFigureRef,numberOfPoint))

	exactTableRef = Report.table("Comparison of route calculation",[
		["Number of points"]+exactResults["numberOfPoints"],
		["Number of possible routes"]+exactResults["numberOfRoutes"],
		["Computation time (ms)"]+exactResults["computeTime"],
		["Best route cost (J)"]+exactResults["bestCost"]
		],"l")

	Report.paragraph("Table {} shows the number of possible routes and the resulting computation time given different numbers of nodes. For a standard travelling salesman problem the number of possible routes is defined by $n!$ however in this case the number of route options is equivilent to $(n-2)!$ where $n$ is the number of nodes in each case. This is due to the start and end node being defeined, thus the complexity is reduced by two nodes. The number of routes directly realtes to the computation time.".format(exactTableRef))
	Report.paragraph("The computation time of the exact TSP is far exceeeding what would be practical for this project therefore the performance has to be increased to producee workable routes from the number of nodes required. These approaches involve producing a best guess and improving upon that which is call heroustics. The approach taken in this project is taken from considering the best routes in figure {} generally comprise of a climbing component and a decending component.".format(exactFigureRef))

	sectionRefs["improve"] = Report.section("Improving Travelling Salesman","sub")
	Report.paragraph("The progressive travelling salesman is an approach to computing a best guess route for the least energy route for a number of points. The computation process is as follows")
	Report.list([
		"Order the nodes by there vertical location from lowest to highest",
		"Consider a subset of the lowest nodes for routing"
		"Compute all permutations to two routes through the subset",
		"Compare all to return the least cost combination",
		"Add first nodes of both routes to final route",
		"Consider a subset of the lowest nodes that are not in the final route and reitterate",
		"Work through all nodes until no nodes are left without a route"
		],"enumerate")

	nodesPerRoutes = [2,3,4,5]
	solutionLines = {}
	progressiveResults = {"nodesPerRoutes":nodesPerRoutes,"computeTime":[],"bestRoute":[],"bestCost":[]}
	#load latin hypercube of required nodes
	nodes = latinHypercube.unitCube(numberOfPoint)
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
	Report.paragraph("Table {} shows the varying computation time for routes through a {} node latin hypercube that have a differnet numbers of nodes in each subset. Where subset refers to the number of nodes that are consideered in each progressive itteration of the code.".format(progressiveTableRef,numberOfPoint))

	title = "Histogram of {} node route costs".format(numberOfPoint)
	filename = plot.histogram(costs,title,"Cost","Frequency",solutionLines)
	histRef = Report.figure(filename,title)
	Report.paragraph("Figure {} shows a histogram of differnt route costs for a {} node latin hypercube. The lines on this histogram plot represent the best cost routes with different numbers of nodes in the subset. It can be seen that the more nodes considered in the subset the closer the result is to that of the exact travelling salesman problem.".format(histRef,numberOfPoint))

def progressivePlanning():
	"function to compile report on progressive path planning"

	print("progressivePlanning")

	sectionRefs["progressive"] = Report.section("Progressive Travelling Salesman","sub")
	nodesPerRoute = 4
	Report.paragraph("In section {} a best guess approach to the travelling salesman was presented and compared with the exact results. Given the results were close enough to the optimum even when the progressive algorithem only considered 2 nodes in the route it can be brought forward to be considered in reference to larger route problems. In these routes {} nodes are considered for both the up route and the down route are used at each stage of the progressive algorithm.".format(sectionRefs["progressive"],nodesPerRoute))

	numberOfPoints = hypercubesConsidered
	captions = []
	filenames = []
	progressiveResults = {"numberOfPoints":numberOfPoints,"computeTime":[],"bestCost":[]}
	for numberOfPoint in numberOfPoints:
		#load latin hypercube of given nodes
		nodes = latinHypercube.unitCube(numberOfPoint)
		#time how long it takes to calculate all routes
		tic = time.time()
		bestRoute,bestCost = travellingPlane.progressiveRoute(nodes,nodesPerRoute)
		toc= time.time()
		#populatee results
		computeTime = round(toc-tic,3)*1000
		progressiveResults["computeTime"].append(computeTime)
		progressiveResults["bestCost"].append(round(bestCost,2))
		#obtain ordered nodes from best route
		orderedNodes = travellingPlane.orderNodes(nodes,bestRoute,True)
		[x,y,z] = changeArray(orderedNodes)
		#plot the resulting route
		captions.append("{} Nodes".format(numberOfPoint))
		filename = plot.line3(x,y,z,"Progressive TSP of {} Nodes".format(numberOfPoint))
		filenames.append(filename)

	caption = "Exact routes calculated by travelling salesman"
	progressiveFigureRef,progressiveFigureRefs = Report.figures(filenames,caption,captions)
	Report.paragraph("Figure {} shows a number of optimal routes for varing numbers of nodes whos order is defined be the progressive travelling salesman algorithm. Though the {} node route is difficult to see the exact routing the other routes show a logical approach to the routing problem. These routes are around the same Latin Hypercubes as seen in Section {}.".format(progressiveFigureRef,numberOfPoint,sectionRefs["latin"]))

	progressiveTableRef = Report.table("Comparison of progressive route calculation",[
		["Number of points"]+progressiveResults["numberOfPoints"],
		["Computation time (ms)"]+progressiveResults["computeTime"],
		["Best route cost (J)"]+progressiveResults["bestCost"]
		],"l")
	Report.paragraph("Table {} shows the computation time and route cost for the differnt routing situations. The computation time is far bellow that of the exact travelling salesman algorithm due to the complexity of this problem being broken down into {} node chunks. Therefore {} nodes were considered in each subset. Looking at the computation time this is a sustainable method for computing routes through greater numbers of nodes as the time required does not grow exponentially.".format(progressiveTableRef,nodesPerRoute,nodesPerRoute*2))

def pathPlanning():
	"function to compile the path planning component of the report"

	print("pathPlanning")

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

	#plot examples of dubin paths with straight line segments
	startNode,startDirection,endNode,endDirection,radius = (0,0),(0,1),(-4,-2),(1,0),1
	pathTypes = ['RSR','LSL','RSL','LSR']#,'RLR','LRL']
	paths = {}
	for pathType in pathTypes:
		(distance,height),path = dubinPath.dubinPath(startNode,startDirection,endNode,endDirection,radius,pathType)
		if path: paths["{0:s} - {1:0.1f}m".format(pathType,distance)]  = path
	arrows={
		"Start":[startNode[0],startNode[1],startDirection[0],startDirection[1]],
		"End":[endNode[0],endNode[1],endDirection[0],endDirection[1]]
		}
	title = "Dubin Paths Comprised of Turns and Straight Line Segments"
	filename = plot.path(paths,title,arrows=arrows)
	dubinCSCRef = Report.figure(filename,title)

	Report.paragraph("Figure {} shows the possible routes from the point {} in direction {} to the point {} in direction {}. The arrows symbolise the start and end headings and the different coloured route symbolise the different routes. In this example the routes comprise of maximum rate turns of radius {} and straight line segment. At close proximity these routes are not always possible".format(dubinCSCRef,startNode,startDirection,endNode,endDirection,radius))

	#plot examples of paths with only turns
	startNode,startDirection,endNode,endDirection,radius = (0,0),(0,1),(2,-1),(1,0),1
	pathTypes = ['RLR','LRL']
	paths = {}
	for pathType in pathTypes:
		(distance,height),path = dubinPath.dubinPath(startNode,startDirection,endNode,endDirection,radius,pathType)
		if path: paths["{0:s} - {1:0.1f}m".format(pathType,distance)]  = path
	arrows={
		"Start":[startNode[0],startNode[1],startDirection[0],startDirection[1]],
		"End":[endNode[0],endNode[1],endDirection[0],endDirection[1]]
		}
	title = "Dubin Paths Comprised of Turns"
	filename = plot.path(paths,title,arrows=arrows)
	dubinCCCRef = Report.figure(filename,title)

	Report.paragraph("Figure {} shows the possible routes from the point {} in direction {} to the point {} in direction {}. The arrows symbolise the start and end headings and the different coloured route symbolise the different routes. In this example the routes only comprise of maximum rate turns of radius {}. These routes are only viable when the distance between points is $D<4r$ where $D$ symbolises the distance.".format(dubinCSCRef,startNode,startDirection,endNode,endDirection,radius))

	nodesPerRoute = 4
	numberOfPoint = 10
	paths={}

	nodes = latinHypercube.unitCube(numberOfPoint)
	bestRoute,bestCost = travellingPlane.progressiveRoute(nodes,nodesPerRoute)
	orderedNodes = travellingPlane.orderNodes(nodes,bestRoute)
	x,y,z = changeArray(orderedNodes)
	paths["Node Order"] = [x,y,z]

	currentPath = dubinPath.DubinPath(planeData["Turn Radius"])
	for node in orderedNodes:
		currentPath.addNode(node)
	paths["UAV Route"] = currentPath.getPath()

	title = "UAV node order and route for a {} node Latin Hypercube".format(numberOfPoint)
	filename = plot.path3(paths,title)

	uavRouteRef = Report.figure(filename,title)
	Report.paragraph("Figure {} shows the optimal path and route for a UAV to circumnavigate a {} node Latin Hypercube. The route is calculated before the path and then the path is calculated from the heading at each node in the route.".format(uavRouteRef,numberOfPoint))

	numberOfPoint = 20
	paths={}
	nodes = latinHypercube.unitCube(numberOfPoint)
	bestRoute,bestCost = travellingPlane.progressiveRoute(nodes,nodesPerRoute)
	orderedNodes = travellingPlane.orderNodes(nodes,bestRoute)
	x,y,z = changeArray(orderedNodes)
	paths["Node Order"] = [x,y,z]
	currentPath = dubinPath.DubinPath(planeData["Turn Radius"])
	for node in orderedNodes:
		currentPath.addNode(node)
	paths["UAV Route"] = currentPath.getPath()
	title = "UAV node order and route for a {} node Latin Hypercube".format(numberOfPoint)
	filename = plot.path3(paths,title)
	uavRouteRef = Report.figure(filename,title)
	Report.paragraph("Figure {} shows the optimal path and route for a UAV to circumnavigate a {} node Latin Hypercube. The route is calculated before the path and then the path is calculated from the heading at each node in the route.".format(uavRouteRef,numberOfPoint))

	#comparison of path and route lengths
	numberOfPoints = [10,20,40,80,160,320,640]#,1280]
	#vary radius 
	numberOfTest = 5
	turnPercent = 0.1
	radiuses = numpy.linspace(0,turnPercent,numberOfTest)
	#configure collection for plotting
	xAxis = []
	yAxis = {}
	lines = {}

	for radius in radiuses:
		yAxis["{:0.1%}".format(radius)]=[]

	for numberOfPoint in numberOfPoints:
		#configure nodes and route
		nodesPerRoute = 4
		nodes = latinHypercube.unitCube(numberOfPoint)
		bestRoute,bestCost = travellingPlane.progressiveRoute(nodes,nodesPerRoute)
		nodes = travellingPlane.orderNodes(nodes,bestRoute)
		routeDistance,routeHeight = travellingPlane.routeDistance(nodes,True)
		xAxis.append(routeDistance)

		pathDistances = []
		for radius in radiuses:
			currentPath = dubinPath.DubinPath(radius)
			for node in nodes:
				currentPath.addNode(node)
			pathDistance = currentPath.getDistance()
			pathDistances.append(pathDistance)
			yAxis["{:0.1%}".format(radius)].append(pathDistance)

		lines["{} Nodes".format(numberOfPoint)]=[(routeDistance,routeDistance),(min(pathDistances),max(pathDistances))]

	title = "Comparison of Path and Route Length for Varyed Nodes and Turning Radiuses"
	filename = (plot.scatter(xAxis,yAxis,title,xLabel="Route Length (m)",yLabel="Path Length (m)",lines=lines))
	pathRouteRef = Report.figure(filename,title)

	Report.paragraph("Figure {:s} shows the relationship between the route length and path length for a number of differnt latin hypercubes. For each latin hypercube the distance of the shortest route (route through of nodes that does not take into account the flight charactersitics of the plane) is calculated and a number of shortest paths (path through ordered nodes that takes into account the maximum turning radius of the airplane). The shortest paths are considerede with turning radiuses varied between ${:0.0%}$ and ${:0.0%}$ of the length of the side of the area that is being explored. For this analysis the area of interest is a unit cube and the percentage value represents the maximum turning radius of the plane over the length of one axis.".format(pathRouteRef,0,turnPercent))

	Report.paragraph("It can be seen from figure {} that as the number of nodes in the latin hypercube is increased (vertical coloured lines indicate a set of tests on a single latin hypercube) the afect of increased turing radius (turning radius is indicated by sets of coloured points) also increases. For the case where the turning radius is $0%$ the path length and route length are the same as the UAV can affectively turn on the spot.".format(pathRouteRef))

	m = []
	for radius in radiuses:
		m.append(numpy.polyfit(xAxis,yAxis["{:0.1%}".format(radius)],1)[0])

	(mm,mc) = numpy.polyfit(radiuses,m,1)

	name = "Path Distance Equation"
	equation = "L_P = ({:0.2f}R + {:0.2f})L_R".format(mm,mc) #" + {:0.2f}R + {:0.2f}".format(cm,cc)
	equationFitRef = Report.equation(name,equation)

	# xAxis = numpy.linspace(0,500,100)
	# yAxis = {}
	# radiuses = numpy.linspace(0,0.2,10)
	# for radius in radiuses:
	# 	yAxis["{:0.1%}".format(radius)] = (mm*radius+mc)*xAxis

	# plot.line(xAxis,yAxis,show=True)

	Report.paragraph("Equation {} shows the relationship between route length and path length given varied turning radiuses. This equation should not be relied upon for exact path planning however is sufficient to see the relationship between the route and path length. Given the linear relationship it can also be determined that the route length is sufficient to calculate when considering the initial costs of paths.".format(equationFitRef))

def sampleSpace():
	"function to complie the section of the report concerened with sample space"

	print("sampleSpace")

	numberNodes = [4,5,6,8,10,11,12,20,25,30,40,50,60,70,80,90,100,160,200,250,320,400,600,1000,1250,1280]
	maxLength = 1000
	numberTest = 100
	testCases = latinHypercube.sampleSpace(maxLength,maxLength,maxLength,numberTest)

	for numberNode in numberNodes:
		filename = "results/route_path_lengths_L_{}_N_{}_T_{}.csv".format(maxLength,numberNode,numberTest)
		try:
			data = loadData(filename)
		except FileNotFoundError:
			data = {"X":[],"Y":[],"Z":[],"Area":[],"Volume":[],"Distance":[],"Height":[],"Energy":[]}
			for testCase in testCases:
				[X,Y,Z] = testCase
				nodes = latinHypercube.sampleSpace(X,Y,Z,numberNode)
				route,energy = travellingPlane.progressiveRoute(nodes)
				orderedNodes = travellingPlane.orderNodes(nodes,route)
				distance,height = travellingPlane.routeDistance(orderedNodes)

				area = X*Y
				volume = X*Y*Z
				data["X"].append(X)
				data["Y"].append(Y)
				data["Z"].append(Z)
				data["Area"].append(area)
				data["Volume"].append(volume)
				data["Distance"].append(distance)
				data["Height"].append(height)
				data["Energy"].append(energy)
			saveData(filename,data)

		#title = "Scatter plot of varying route and path lengths for a {} node latin hypercube".format(numberNode)
		#plot.scatter(data["Volume"],{"Route Length":data["Distance"],"Total Height":data["Height"]},title,xLabel="Research Volume (m^3)",yLabel="Length (m)")
		#plot.scatter3(data["Area"],data["Z"],data["Distance"],title,xLabel=r"Research Area [$X \times Y$](m^2)",yLabel="Reseach Height (m)",zLabel="Route Distance (m)",show=True)

def conclusion():
	"function to add the conclusion section to the report"

	print("conclusion")

	Report.bibliography()

if __name__ == "__main__":
	# introduction()
	# method()
	# exactPlanning()
	# progressivePlanning()
	# pathPlanning()
	sampleSpace()
	# conclusion()