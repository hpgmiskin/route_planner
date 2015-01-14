from shared import *
import scipy,numpy
from reportCalculations import *
import texDocument,latinHypercube,travellingPlane,dubinPath,dubinPathOld,planeEnergy,airFoil,nodeResults,buildModel,plot,time
hypercubesConsidered = [10,20,60,100]

class ReportContent(texDocument.TexDocument):
	"extends TexDocument "

	def __init__(self,arg):
		super(self.__class__, self).__init__(arg)

	def titlePage(self):
		print("titlePage")

		title = "Gathering Atmospheric Data"
		subtitle = "Using an Unmanned Air Vehicle"
		abstract = "This report looked at energy based path planning for atmospheric data collection using unmanned air vehicles in a predetermined area, with particular consideration to the sample quality of data collected. Sampling plans were used in combination with route planning algorithms to produce optimal routes through a sample area. These routes were related to the energy consumed to produce a model that allows energy based path planning. The model for energy based path planning was found to be viable for certain plane configurations."
		integrity = "This report is submitted in partial fulfilment of the requirements for the Degree of Bachelor / Master of Engineering, Faculty of Engineering and the Environment, University of Southampton"
		self.title(title,subtitle,abstract,integrity)

		self.updateTex(r"\vfill")
		self.section("Acknowledgements","*")
		self.paragraph("I would like to thank my supervisor Andras Sobester for his help and support on this project, firstly by having the confidence in allowing me to explore in a direction that interested me and secondly by offering much needed support at many stages through this process. As a result I have found the work that I have done both interesting and rewarding. I am proud to put my name to this piece of work and know that this would not be the case without the support given.")
		self.updateTex(r"\vfill")
		self.updateTex(r"\clearpage")
		self.contents(True)

		self.abreviations = {
			"UAV":"Unmanned aerial vehicle",
			"TSP":"Travelling salesman problem",
			"DTSP":"Dubins travelling salesman problem"
		}
		self.nomeclature = {
			r"m":["Mass",r"kg"],
			r"R":["Turning Radius",r"m"],
			r"\beta":["Energy Coefficient",r"1"],
			r"\gamma":["Energy Factor",r"N"],
			r"c":["Wing Chord",r"m"],
			r"g":["Acceleration due to Gravity",r"m \cdot s^-2"],
			r"b":["Wing Span",r"m"],
			r"Re":["Reynolds Number",r"1"],
			r"\mu":["Air Viscosity",r"Pa \cdot s"],
			r"\rho":["Air Density",r"kg \cdot m^-3"],
			r"S":["Wing Planform Area",r"m^2"],
			r"A":["Aspect Ratio",r"1"],
			r"V":["Flight Velocity",r"m \cdot s^-1"],
			r"\alpha":["Angle of Attack",r"degrees"],
			r"C_L":["Coefficient of Lift",r"1"],
			r"C_D":["Coefficient of Drag",r"1"],
			r"C_{D_0}":["Coefficient of Zero Lift Drag",r"1"],
			r"C_{D_i}":["Coefficient of Induced Drag",r"1"],
			r"L/D":["Lift to Drag Ratio","1"],
			r"e":["Oswald Factor",r"1"],
			r"x":["Longitude Coordinate",r"m"],
			r"y":["Latitude Coordinate",r"m"],
			r"z":["Altitude Coordinate",r"m"],
		}

	def introduction(self):
		print("introduction")

		self.paragraph("Unmanned aerial vehicles (UAVs) are used to collect atmospheric data, the flightpath taken by the UAV to collect this data defines where the atmospheric reading of interest is sampled. The locations at which atmospheric data is sampled determines the quality of model that can be produced from the readings. To ensure that the route taken by the UAV is optimal in terms of the quality of data collected, this report utilises optimal sampling plans to define the locations that the UAV should pass through. Then to ensure that the UAV is able to collect as much data as possible, the route through the sample plan is optimised to reduce the energy cost of the route. In this report atmospheric data refers to a meteorological reading to be collected.")

	def aimsObjectives(self):
		print("aimsObjectives")

		self.section("Aims","sub")
		self.paragraph("The aim of this project is to research, design and implement a UAV path planner that minimises energy consumption while optimising spread and depth of data collection.")

		self.section("Objectives","sub")
		self.paragraph("The following objectives define the measurable goals of the project required to fully complete the aim. The objectives are listed in the order of completion, where each objective is a prerequisite to the next.")
		self.list([
			"Design a model to calculate the energy costs of flight between two points in space. This model will output the predicted energy required from the work done against drag and the change in gravitational energy.",
			"Implement an algorithm that uses the energy model to compare the cost of different routes to result in the least energy consumed.",
			"Consider the flight characteristics of the UAV to produce a navigable path which visits the waypoints in order, as defined by the route to produce an accurate flight plan and energy prediction.",
			"Fit the results of flight plans in different sample areas to the resulting energy consumed to produce a model that enables optimal path planning based on the area of interest and total UAV energy."],"enumerate")

	def problemOutline(self):
		print("problemOutline")

		self.section("Problem Outline","sub")  
		self.paragraph(r"The troposphere is the lowest atmospheric layer and of significant interest to meteorological researchers as ``almost all weather develops in the troposphere'' \cite{NatGeo}. The section of the troposphere that is closest to the earth is the atmospheric boundary layer, in this layer the atmospheric conditions are affected by the surface of the earth. These effects mean that modelling this section is much more complicated than other layers of the atmosphere, therefore ``the boundary layer is still not represented realistically'' \cite{Teixeira2008}. Developing a greater understanding and thus better modelling of the atmospheric boundary layer will improve the ability to predict weather patterns and pollutant dispersion, to name but two benefits.")
		self.paragraph(r"To collect atmospheric data a number of approaches have been used historically, ``many years before the use of radio-controlled aircraft, the collection of in-situ measurements was primarily done with balloons, towers, and tethersondes' \cite{Bonin2011}. These options were limited as they were not able to move within the area of interest to build a model. UAVs operate with ``reduced human risk, but also reduced weight and cost, increased endurance, and a vehicle design not limited by human physiology'' \cite{Pepper2012} in comparison to their manned counterparts. This means they provide a cheap and mobile data collection platform.")
		self.paragraph(r"There are 5 main classes of UAV for different requirements \cite{Sarris2001}; the class of UAV best suited to collecting atmospheric data of a limited area is the close range class. This class of UAV: ``require minimum manpower, training, and logistics, and will be relatively inexpensive'' \cite{FasDod}. These benefits allow a greater number of researchers to have access to mobile data collecting platforms. Most small UAVs are ``not capable of reaching above 5,000ft [1524m]'' \cite{Weibel2005} with their maximum range being less than 10km \cite{Blyenburgh2000}.")

	def literatureReview(self):
		print("literatureReview")

		self.section("Literature Review","sub")
		self.paragraph(r"To achieve the objectives presented in this project pre-existing material on energy modelling, tour planning, path planning, energy routing and sampling plans has to be considered.")
		self.paragraph(r"\citen{M.Price2006} consider the design parameters that affect aircraft performance and detail considerations to increase the efficiency. The $L/D$ ratio is identified along with the weight as driving parameters for aircraft range. \citen{Asselin1997} however looks at the top level aerodynamic equations of flight to provide equations capable af defining energy consumption under different flight modes. Together they provide for an overview of flight efficiency and basic equations to estimate this. \citen{Raymer2006} looks further into aerodynamic equations of flight and presents an estimate for the Oswald Factor for standard airframes which is required in a number of the aerodynamic equations.")
		self.paragraph(r"\citen{Bigg1976,Held1984,DeBerg2010} calculate minimum length tours of more than two points through applying the Travelling Salesperson Problem (TSP). The TSP is concerned with ``finding the shortest path joining all of a finite set of points whose distances from each other are given'' \cite{Held1984}. The TSP problem considered in these papers uses the euclidean distance where the ``euclidean distances satisfy the triangle inequality'' \cite{DeBerg2010}; ``The triangle inequality implies that no reasonable salesman would ever revisit the same city: instead of returning to a city, it is always cheaper to skip the city and to travel directly to the successor city'' \cite{DeBerg2010}. Given the euclidean distances the solutions obtained do not correspond to the shortest path for a either a energy based TSP or a Dubins Travelling Salesman Problem (DTSP)")
		self.paragraph(r"\citen{Dubins1957,Boissonnat1993} consider the shortest path of a vehicle with a bounded turning radius in two dimensions: given a trajectory and location for the beginning and end points. Both papers found that the minimum path is comprised of maximum rate turns and straight line segments. This initial work on shortest paths is extended by \citen{Chitsaz2007} to take a third dimension into account: for low altitude ranges the shortest path is the Dubins path in the x-y plane and a constant rate altitude climb. High altitude climbs diverged from the Dubins path due to helical climbing component; however this is not relevant as only low altitude climbs are considered in this project.")
		self.paragraph(r"\citen{McGee2005,Techy2009} apply Dubins shortest path in uniform wind. This is done by considering a ground reference frame and wind reference frame which results in the Dubins minimum path being calculated in the wind reference frame. The maximum rate turns in the air frame of reference ``correspond to trochoidal paths in the inertial (ground) frame'' \cite{Techy2009}. Assuming uniform and time-invariant wind leads to potential inaccuracies which are considered through using 'a turning rate less than the actual maximum turning rate' \cite{McGee2005}. Both papers considered utilise different approaches to obtain a final optimal path, though the resulting optimal paths are both comprised of a combination of trochoidal path sections and straight line sections. These papers present an extension of the Dubins path concept to consider wind but also outline the added complexity of uniform wind without resulting in a vastly different path.")
		self.paragraph(r"\citen{Savla2005a,Savla2005,LeNy2008} consider the DTSP. The basic approach considered in all papers is in the form of the alternating algorithm which requires calculation of a minimum tour using euclidean distances for an initial ordering. From the initial order the heading at nodes is given by the direction of either the vertex before the node or the vertex after the node. With the order, location and heading defined at each point the Dubins shortest path can be calculated. \citen{Savla2005} goes on to consider stochastic DTSP where the points are normally distributed and puts forth a bead tilling algorithm to improve the performance which is an important consideration for the initial planning aspect of this paper. \citen{LeNy2008} however goes beyond the scope of this paper in considering variable vehicle dynamics.")
		self.paragraph(r"\citen{Al-Sabban,Chakrabarty2009,Langelaan2007} look into the minimum energy paths through non-uniform wind vectors by considering the total energy of the UAV and attempting to minimise the reduction in energy. \citen{Al-Sabban} uses a markov decision process to plan a route through time varying wind vectors which have a degree of uncertainty. \citen{Chakrabarty2009,Langelaan2007} however use a predetermined knowledge of the wind with the aim to exploit atmospheric energies. The given equations of energy and considerations of optimal routes through complex wind fields applies directly to this paper; however attempting to tap into soaring flight is not feasible given the requirement to fully investigate a particular research area.")
		self.paragraph(r"\citen{Forrester2008,McKay2000} consider efficient sampling plans for black box experiments to improve the quality of the model produced. Both papers present Latin hypercube sampling to be an improvement on random sampling as they ensure ``that each of those components is represented in a fully stratified manner'' \cite{McKay2000} where those components refer to input dimensions. \citen{Forrester2008} extends this by optimising Latin hypercubes to result in the plan with best space fillingness. The sampling plans provided can easily be utilised in the primary planning component of the UAV tour in this project. \citen{AlexanderI.J.Forrester2009} additionally looks at adding samples to existing surrogates to improve the quality of the model produced. These papers provide the basis for optimal sampling plans for both initial data collection and subsequent flights given an existing model. This outlines the importance of a versatile path planner that can cover an area of interest in addition to any collecting of nodes no matter how sparse.")

	def latinHypercubeSampling(self):
		print("latinHypercubeSampling")

		self.section("Latin Hypercubes","sub")
		self.paragraph("Latin hypercubes are sampling plans that provide the best space fillingness while limiting the total number of sampling points required. This is generally applied to testing of computer simulations where the collection of each point is expensive. In this situation however the travel between the points is the expensive component.")

		numberOfNodes = hypercubesConsidered
		filenames,captions = [],[]
		for numberOfNode in numberOfNodes:
			nodes = latinHypercube.unitCube(numberOfNode)
			[x,y,z] = changeArray(nodes)
			title = "{} Node Plan".format(numberOfNode)
			filename = plot.scatter3(x,y,z,title.format(numberOfNode))
			filenames.append(filename)
			captions.append(title)
		caption = "Latin Hypercubes with Varying Numbers of Nodes"
		latinFigureRef,LatinFigureRefs = self.figures(filenames,caption,captions)

		self.paragraph(r"Figure {} shows Latin hypercubes with varying numbers of nodes. The nodes within the Latin hypercubes are located in such a way that ensures along each vertex the nodes are equally spaced and the spread of the nodes is maximised. The resulting plans are therefore efficient sampling plans that are space filling within the area of interest. The Latin hypercubes shown here are computed within MATLAB using code from the work of \citen{{Forrester2008}} and imported into python for utilisation within this project. Once a Latin hypercube is computed the result is cached so for any following calls MATLAB is not required to be called.".format(latinFigureRef))
		self.paragraph("Given that data collection is rarely within a unit cube and more likely on the scale of thousands of meters in a research area that is far from a cuboid, these sample plans need to be altered for use. To apply these Latin hypercubes to provide sampling plans for any research area they can be stretched in each vertex.")

		filenames,captions = [],[]
		numberNode = 100
		xLengths,yLengths,zLengths = [777,534,71,54],[925,68,86,543],[968,506,937,93]
		for i in range(4):
			xLength,yLength,zLength = xLengths[i],yLengths[i],zLengths[i]
			nodes = latinHypercube.sampleSpace([xLength,yLength,zLength],numberNode)
			[x,y,z] = changeArray(nodes)
			title = "{} x {} x {}".format(xLength,yLength,zLength)
			filename = plot.scatter3(x,y,z,title,scaleBox=True)
			captions.append(title)
			filenames.append(filename)
		caption = "Stretched {} Node Latin Hypercubes".format(numberNode)
		stretchedCubeRef,stretchedCubeRefs = self.figures(filenames,caption,captions)

		self.paragraph("Figure {} shows a number of {} node Latin hypercubes stretched to varying research areas. It can be seen that the data spread of the Latin hypercubes remains the same along each of the vertexes; however in terms of actual distance between nodes in the sampling plan this causes bunching. This results in data that is equally sampled for each input variable therefore the effect of each variable on the model is equally considered.".format(stretchedCubeRef,numberNode))

	def exactTravellingSalesman(self):
		print("exactTravellingSalesman")

		self.section("Exact Travelling Salesman","sub")
		self.paragraph("To calculate the least cost tour of a number of nodes the TSP presents itself. The TSP is well documented for many route planning problems, both for two dimensions and three dimensions. The standard form of the TSP is to calculate the least cost of visiting every node where the cost is defined as the euclidean distance between nodes. Due to the euclidean properties of the TSP there are many heuristic approaches to computing best guess solutions.")
		self.paragraph("Without the utilisation of heuristic approaches the TSP is a very computationally expensive problem. This is due to the number of routes that are possible given even a small number of nodes. The number of routes increase by a factor of the total number of nodes each time a node is added to the computation. This is due to that new node needing to be considered at every point in every existing route.")

		nodes = [[-1,0],[-0.5,0.866],[0.5,0.866],[1,0],[0.5,-0.866],[-0.5,-0.866]]
		numberNodes = len(nodes)
		lines = [[],[]]
		for i in range(numberNodes):
			for j in range(numberNodes):
				if ((i == j) or (i == j+1) or (i == j-1) or (i+1 == j) or (i-1 == j) or ((i == 0) and (j==numberNodes-1)) or ((j == 0) and (i==numberNodes-1))):
					pass
				else:
					lines[0].append(nodes[i][0])
					lines[0].append(nodes[j][0])
					lines[1].append(nodes[i][1])
					lines[1].append(nodes[j][1])

		numberConnections = sum(range(numberNodes))
		numberRoutes = int(scipy.misc.factorial(numberNodes))

		nodes.append([-1,0])
		xy = changeArray(nodes)
		series = {"All Connections":lines,"Shortest Route":xy}
		title = "Connections and Shortest Route through {} Nodes".format(numberNodes)
		filename = plot.path(series,title,tight=False)
		tspRouteRef = self.figure(filename,title)

		self.paragraph("Figure {} shows an arrangement of nodes with all possible connections shown in blue and the shortest route in green. The number of connections between {} nodes route is {}. Given that the number of routes through these connections totals to {} this shows how the TSP can easily become unmanagable.".format(tspRouteRef,numberNodes,numberConnections,numberRoutes))
		self.paragraph("The optimal route is a found using python. A matrix of the length of all connections is calculated using the euclidean distance, then the route distances are found from summing up the individual connection distances from the distance matrix. For all permutations of node ordering, the length of the path is computed and the shortest route is selected.")
		self.paragraph("For the route planning in this report it is imperative to devise a TSP solution that provides a best guess method to finding a least cost route. This is because the number of nodes required for a sampling plan to achieve a high quality model will far exceed 10 nodes, resulting in excessive computation time.")

	def dubinPathPlanning(self):
		print("dubinPathPlanning")

		self.section("Dubins Paths","sub")
		self.paragraph("The shortest path between two locations when considering purely a start and end location is the euclidean distance between each node. This is the distance that would be experienced by a vehicle that can travel in any direction regardless of current heading. To work out the path length between two points where the start and end directions are determined is a more complicated problem. This requires the considering of the minimum turning radius for the vehicle in question.")
		self.paragraph("A Dubins path is a minimum distance path between a given start position and direction and a given end position and direction. There are a number of different forms of Dubins paths that can be achieved and the minimum path is the minimum of the Dubins paths that can be computed. These paths are comprised of maximum rate turns and straight line segments.")
		self.list([
			"RSR - Right Turn, Straight Travel then Right Turn",
			"RSL - Right Turn, Straight Travel then Left Turn",
			"LSR - Left Turn, Straight Travel then Right Turn",
			"LSL - Left Turn, Straight Travel then Left Turn",
			"RLR - Right Turn, Left Turn then Right Turn",
			"LRL - Left Turn, Right Turn then Left Turn",
			])
		self.paragraph("To calculate the different Dubins paths that are possible geometric relations and vector identities can be utilised. The initial stage is to consider the start and end directions. For both the start and end directions the circles that correspond to maximum rate turns are computed. That is the circle where the initial direction is tangential to the circumference and the circles where the final direction is tangential to their circumference.")
		self.paragraph(r"These paths are calculated in python using the logic detailed by \citen{Giese2012} to determine the geometric and draw respective paths. The shortest path is then selected by comparing the resulting distances.")
		self.paragraph("For the routes with a straight line segment in the middle, tangent lines are computed. These four sets of lines that are tangential to a start and end circle make up the straight section of the route. The complete path is the combination of an arc that lies in the circumference of the start circle, the straight line section to the end circle and then an arc in the circumference of the end circle. For some cases where the start and end points are close some path types are not achievable.")

		filenames,titles = [],[]
		startNodeA,startDirectionA,endNodeA,endDirectionA,radius = (0,0),(0,1),(-4,-2),(1,0),1
		arrows={"Start":startNodeA+startDirectionA,"End":endNodeA+endDirectionA}
		pathTypes = ['RSR','LSL','RSL','LSR']
		paths = {}
		for pathType in pathTypes:
			(distance,height),path = dubinPathOld.dubinPath(startNodeA,startDirectionA,endNodeA,endDirectionA,radius,pathType)
			if path: paths["{0:s} - {1:0.1f}m".format(pathType,distance)]  = path
		title = "Turn Straight Turn"
		filename = plot.path(paths,title,arrows=arrows)
		titles.append(title)
		filenames.append(filename)

		startNodeB,startDirectionB,endNodeB,endDirectionB,radius = (0,0),(0,1),(2,-1),(1,0),1
		arrows={"Start":startNodeB+startDirectionB,"End":endNodeB+endDirectionB}
		pathTypes = ['RLR','LRL']
		paths = {}
		for pathType in pathTypes:
			(distance,height),path = dubinPathOld.dubinPath(startNodeB,startDirectionB,endNodeB,endDirectionB,radius,pathType)
			if path: paths["{0:s} - {1:0.1f}m".format(pathType,distance)]  = path
		title = "Turn Turn Turn"
		filename = plot.path(paths,title,arrows=arrows)
		titles.append(title)
		filenames.append(filename)

		title = "Dubins Paths Comprised of Turns and Straight Line Segments"
		dubinPathRef,[dubinPathRefA,dubinPathRefB] = self.figures(filenames,title,titles)

		self.paragraph("Figure {} shows the possible routes from the point {} in direction {} to the point {} in direction {}. The arrows symbolise the start and end headings and the different coloured route symbolise the different routes. In this example the routes comprise of maximum rate turns of radius {} and straight line segment.".format(dubinPathRefA,startNodeA,startDirectionA,endNodeA,endDirectionA,radius))
		self.paragraph("To calculate the paths that are comprised of only maximum rate turns the start and end circles are used again. The circles that lie with their circumference tangential to both a start and end circle is used to determine the points of change from one turn direction to the other. The path then follows the circumference of each of the three circles in turn. Paths of only maximum rate turns are only viable when $D<4r$ where $D$ symbolises the distance between the start and end points, as above this distance the radius would need to increase to be navigable using only three circles.")
		self.paragraph("Figure {} shows the possible routes from the point {} in direction {} to the point {} in direction {}. The arrows symbolise the start and end headings and the different coloured route symbolise the different routes. In this example the routes only comprise of maximum rate turns of radius {}.".format(dubinPathRefB,startNodeB,startDirectionB,endNodeB,endDirectionB,radius))

	def method(self):
		print("method")

		self.paragraph("To achieve the objectives of this project a particular process had to be followed. This ensured that each further level of investigation was based on completion of the one preceding it. The initial goal was to design a simple yet effective energy model that could use actual plane data and return the expected energy consumption for a number of flight manoeuvres. Using this energy model as a basis for comparison the computation time of the TSP needed to be improved. Having obtained a least energy route through a sampling plan then create a path through the route that adheres to the UAV flight characteristics.")
		self.paragraph(r"In this section and for the remainder of this report, \textbf{route planning} refers to the ordering of nodes within the sample plan and \textbf{path planning} refers to the creating of navigable paths from this ordering of nodes. The route planning aspect requires ranking of comparative energies, however the path planning component requires more detailed energy considerations.")

	def energyModel(self):
		print("energyModel")

		self.energyModelSectionRef = self.section("Energy Model","sub")
		self.paragraph("To correctly estimate the energy used in navigating through a particular route, an energy model to define how different flight manoeuvres consume energy was required. For a basis of the energy model the plane was assumed to consume energy in two ways: in doing work against drag and by doing work against gravity. As the plane navigates the manoeuvres on its route the consumption reduces the available energy in the plane's battery. Given a good energy model the length of the route can be determined a priori safe in the knowledge that the plane will not run out of energy before completing its route.")
		self.paragraph(r"Obtaining accurate values for the variables required for energy modelling is difficult given an off the shelf UAV. Therefore the energy model was harder to calculate for individual planes. To work around this problem the aerodynamic values for the plane were obtained from results to foil simulations from the internet. This enabled a similar airfoil shape to be selected that allows aerodynamic variables to be easily obtained. The website \textit{airfoiltools.com} contains the results to simple simulations on many airfoils and the data can be pulled for virtually any foil shape at varying Reynolds numbers.")
		energyModelDiagramRef = self.figure("figures/energy_model_diagram.png","Diagram of Energy Model Logic",1)
		self.paragraph("Figure {} shows the logic behind the approach used to compute an energy model using readily available atmospheric and plane variables. The best Reynolds number was then selected an iterative approach which was used to download airfoil coefficients. The following equations were used to produce the energy model.".format(energyModelDiagramRef))
		
		reynoldsEqRef = self.equation("Reynold Number",r"Re = \frac{\rho c V}{\mu}")
		self.paragraph(r"Equation {} was used to calculate the Reynolds number given the flight conditions of the plane. This was required to select the correct data set for obtaining the relevant values for coefficient of lift and the zero lift coefficient of drag.".format(reynoldsEqRef))

		xLabel = r"Angle of Attack $\alpha (degrees)$"
		titleD,titleL = r"Coefficient of Zero Lift Drag $C_{{D_0}}$",r"Coeficient of Lift $C_L$"
		pathsD,pathsL = {},{}
		reynoldsNumbers = [50000,100000,200000,500000,1000000]
		for reynoldsNumber in reynoldsNumbers:
			planeAirFoil = airFoil.AirFoil(planeEnergy.foilName,reynoldsNumber)
			pathsL["Re - {}".format(reynoldsNumber)] = [planeAirFoil.getAoAs(),planeAirFoil.CLs]
			pathsD["Re - {}".format(reynoldsNumber)] = [planeAirFoil.getAoAs(),planeAirFoil.CDs]
		filenameL = plot.path2(pathsL,titleL,xLabel=xLabel,yLabel=titleL)
		filenameD = plot.path2(pathsD,titleD,xLabel=xLabel,yLabel=titleD)

		title = r"$C_L$ and $C_{{D_0}}$ Plots of a {} Airfoil".format(planeEnergy.foilName.upper())
		coffPlotRef,coffPlotRefs = self.figures([filenameL,filenameD],title,[titleL,titleD])

		self.paragraph(r"Figure {} shows the coefficient of drag and coefficient of lift for varying angles of attack. This is data obtained directly from \textit{{airfoiltools.com}} for the {} airfoil operating in conditions with a Reynolds number between {} and {}.".format(coffPlotRef,planeEnergy.foilName.upper(),reynoldsNumbers[0],reynoldsNumbers[-1]))

		maxRangeEqRef = self.equation("Maximum Range Equation",r"C_L = \sqrt{C_{D_0}\pi A e}")
		self.paragraph(r"Equation {} shows the relationship between the coefficient of lift and the zero lift coefficient of drag where the plane's range is a maximum. The data from \textit{{airfoiltools.com}} was then used to find the values of the coefficients where the equation is satisfied. This calculation was only required if the flight velocity of the plane was not defined.".format(maxRangeEqRef))

		velocityEqRef = self.equation("Steady Velocity Equation",r"V=\sqrt{\frac{2mg}{\rho S C_L}}")
		self.paragraph("Equation {} depicts the relationship between velocity and the coefficient of lift. This equation was utilised in two ways. When the velocity of the plane is defined this equation defines the coefficient of lift. When however the coefficient of lift is calculated from equation {} this equation is used to define the velocity.".format(velocityEqRef,maxRangeEqRef))

		dragEqRef = self.equation("Drag Coeficient",r"C_D = C_{D_0} + \frac{C_L^2}{\pi A e}")
		self.paragraph("Equation {} was used to amend the coefficient of drag for a 3 dimensional wing. This utilises the Oswald factor and aspect ratio which are parameters used to define the wing loading and shape profile respectively.".format(dragEqRef))

		loadFactorEqRef = self.equation("Load Factor Equation",r"n=\frac{L}{W}=\sqrt{1+\left(\frac{V^2}{R g}\right)^2}")
		self.paragraph(r"Equation {} shows the relationship between the load factor and the turning radius for the plane. The load factor is the ratio of lift to weight during a turn. This allows the greater energy required in turns to be considered for path planning.".format(loadFactorEqRef))

		levelEnergyEqRef = self.equation("Level Flight Energy",r"E = \frac{1}{2} \rho C_D S V^2 D")
		turnEnergyEqRef = self.equation("Turning Flight Energy",r"E= n\frac{C_D}{C_L} m g D")
		climbEnergyEqRef = self.equation("Climbing Flight Energy",r"E = mg H")

		self.paragraph(r"Equations {}, {} and {} were used to calculate the level, turning and climbing flight consumption of energy respectively. Climbing flight here only considers the work against gravity. Therefore for any form of climbing flight the energy consumption due to drag must also be taken into account. For example if a plane were to fly $1m$ horizontally and $1m$ vertically then the energy used would be found by summing equation {} with $D=\sqrt{{2}}$ and equation {} with $H=1$.".format(levelEnergyEqRef,turnEnergyEqRef,climbEnergyEqRef,levelEnergyEqRef,climbEnergyEqRef))
		self.paragraph("The energy model was then simplified for the route planning. In the route planning the actual energy does not matter but the ranking of energy consumption does. For this reason the accurate equations for energy are reduced to a form where the energy is merely a cost balance between level and climbing flight. This is similar to the $L/D$ ratio.")

		energyEquationRef = self.equation("Energy Equation",r"E =\gamma(\beta D + H)")
		betaEquationRef = self.equation("Beta Equation",r"\beta = \frac{\rho C_D S V^2}{2mg}")
		gammaEquationRef = self.equation("Gamma Equation",r"\gamma = mg")

		self.paragraph(r"Equation {} is the overall energy equation used to calculate accurate energy based on distance and height gain. The constants $\beta$ and $\gamma$ are depicted in equations {} and {} respectively. The energy model has been manipulated in this way to illustrate that the $\gamma$ component is merely a factor applied to the whole equation. Therefore for the purpose of routing the constant $\alpha$ can be used alone to define the energy equation. This abstraction provides for the constant $\gamma$ to not affect route selection. Therefore it can be applied subsequently to calculating the ordering of nodes.".format(energyEquationRef,betaEquationRef,gammaEquationRef))
		self.paragraph(r"From this point forward in the report the energy computation will be referred to in two ways: the \textbf{{cost}} of a route will refer to the component of equation {} contained within the brackets and is an adjusted length measured in meters, the \textbf{{energy}} however refers to the result of the full equation and is measured in joules.".format(energyEquationRef))

	def exactTravellingPlane(self):
		print("exactTravellingPlane")

		self.section("Exact Travelling Plane","sub")
		self.paragraph("The exact travelling plane developes on the TSP to include energy considerations for route planning. Firstly the cost of travel between every possible pair of nodes in the sample plan was calculated. Then for every permutation of how these nodes can be ordered the cost of the overall route was calculated and the least cost selected as the optimal route.")

		beta = 0.1
		numberOfNodes = [4,6,8,10]#,12]
		filenames,captions = [],[]
		exactResults = {"numberOfNodes":numberOfNodes,"numberOfRoutes":[],"computeTime":[],"bestCost":[]}
		for numberOfNode in numberOfNodes:
			#compute results
			filename = "calculations/exact_route_results_cost_{:0.1f}_{}.dat".format(beta,numberOfNode)
			data = loadOrRun(filename,calculateExactRouteResults,beta,numberOfNode)
			#load results into variables
			bestCost = data["bestCost"]
			bestRoute = data["bestCost"]
			exactResults["numberOfRoutes"].append(int(data["numberOfRoute"]))
			exactResults["computeTime"].append(data["computeTime"])
			exactResults["bestCost"].append(data["bestCost"])
			#plot the resulting route
			title = "{} Node Route".format(numberOfNode)
			filename = plot.line3(data["x"],data["y"],data["z"],title)
			captions.append(title)
			filenames.append(filename)
		caption = "Exact Travelling Salesman Routes"
		exactRoutesRef,exactRoutesRefs = self.figures(filenames,caption,captions)
		self.exactRoutesRef = exactRoutesRef
		startEndFactor = 1

		self.paragraph("Figure {} shows the optimal routes for different numbers of nodes. These optimal routes are found by computing the exact cost of each and every route option. Although this yields the shortest route, this approach was not efficient in terms of the computation time required. To enable calculation of a {} node route the start point of the route was defined by the lowest node. This reduces the complexity of the path planning problem to that of a {} node route. ".format(exactRoutesRef,numberOfNode,numberOfNode-startEndFactor))

		exactTableRef = self.table("Comparison of route calculation",[
			["Number of points"]+exactResults["numberOfNodes"],
			["Number of possible routes"]+exactResults["numberOfRoutes"],
			["Computation time (ms)"]+exactResults["computeTime"],
			["Best route cost (m)"]+exactResults["bestCost"]
			],"l")

		self.paragraph(r"Table {} shows the number of possible routes and the resulting computation time given different numbers of nodes. For a standard travelling salesman problem the number of possible routes is defined by $n!$ however in this case the number of route options is equivalent to $(n-{})!$ where $n$ is the number of nodes in each case. This is due to the start node being defined, thus the complexity is reduced by a single node. The number of routes directly relates to the computation time.".format(exactTableRef,startEndFactor))
		self.paragraph(r"The computation time of the exact TSP far exceeds what would be practical for this project; therefore the performance has to be increased to produce workable routes from the number of nodes required. The heuristic approach used in this report is taken from consideration that the best routes in figure {} are generally comprised of a single climbing component and single descending component.".format(exactRoutesRef))

	def progressiveTravellingPlane(self):
		print("progressiveTravellingPlane")

		self.progressiveSectionRef = self.section("Progressive Travelling Plane","sub")
		self.paragraph("From the observation that the optimal routes from figure {} all comprised of an up component and down component, the logic for a best guess approach was devised with far less computation time required. It seemed very logical that a route through nodes in three dimensions would comprise of an up section and down section however it was important to consider the absolute optimal solution.".format(self.exactRoutesRef))
		progressiveRef = self.figure("figures/progressive_travelling_plane_diagram.png","Progressive Travelling Plane Logic",1)
		self.paragraph("Figure {} shows the logic behind the progressive travelling salesman function. The function works using an iterative approach to selecting the optimal route. A small subset of the lowest nodes is analysed at each stage to define the route. Here $n$ defines the number of nodes in each route within the subset. This iterative approach assumes that the least cost route will be comprised of an up component of travel and down component of travel. Upon path planning for each level of the sample area a single point is added to each route. The up route is constructed from beginning to end while the down route is constructed in reverse. When the routes meet at the top, route A and route B are joined to form a single route.".format(progressiveRef))

		beta,nodesPerRoute,numberOfNodes = 0.1,4,hypercubesConsidered
		filenames,captions = [],[]
		for numberOfNode in numberOfNodes:
			filename = "calculations/progressive_route_results_{:0.1f}_{}_{}.dat".format(beta,numberOfNode,nodesPerRoute)
			data = loadOrRun(filename,calculateProgressiveResults,beta,numberOfNode,nodesPerRoute)
			[x,y,z] = data["xyz"]
			title = "{} Nodes Progressive".format(numberOfNode)
			filename = plot.line3(x,y,z,title)
			filenames.append(filename)
			captions.append(title)
		caption = "Exact routes calculated by travelling salesman"
		progressiveFigureRef,progressiveFigureRefs = self.figures(filenames,caption,captions)
		self.paragraph("Figure {} shows a number of optimal routes for varying numbers of nodes whose order is defined by the progressive travelling salesman algorithm. For the {} node route it is difficult to see the exact routing; however for the other routes a logical approach to the routing problem can be seen. The initial progressive travelling plane logic did not produce routes of this quality as the least cost route on the way up would always favour finishing lower down even though in the next iteration this would mean having to gain greater height. Due to this visual identification of problems the cost of travel to the highest node is added to the up path for each iteration. This improvement caused the results that are shown.".format(progressiveFigureRef,numberOfNode))
		self.paragraph("Figure {} displays some imperfections in the calculation of an optimal route. This is due to the significant change in height experienced at the top section of the route (where the routes A and B join up to form a single route). This suggests that figures {} and {} could contain inefficiencies in the route.".format(progressiveFigureRefs[1],progressiveFigureRefs[2],progressiveFigureRefs[3]))


	def planePathPlanning(self):
		print("planePathPlanning")

		self.pathPlanningSectionRef = self.section("Path Planning","sub")
		self.paragraph("The least energy route through a number of nodes has been defined; however this route assumes that the UAV is able to turn on the spot and is not constricted by turning radius. Therefore to compute the actual energy cost of circumnavigating a route the turning radius of the UAV needs to be considered. Dubins paths can be used to produce a path from this route.")
		self.paragraph("To compute a path through a sample volume the altitude of the unmanned aerial vehicle must be taken into consideration. The assumption for this stage in path planning is that the plane considered is able to change its rate of climb quick enough to approximate being instantaneous, whereas the rate of turn is not able to change with the same speed.")
		self.paragraph("To increase the accuracy of this assumption the rate of climb for each section would change gradually from the previous section's rate of climb to the next section's rate of climb. However given the added complexity of this implementation it was assumed that the improvement on accuracy would not be sufficient to warrant the time required.")

		beta,radius,numberOfNodes,nodesPerRoute = 0.1,0.1,[10,20],4
		filenames,titles = [],[]
		for numberOfNode in numberOfNodes:
			filename = "calculations/dubin_path_results_{:0.1f}_{:0.2f}_{}_{}.dat".format(beta,radius,numberOfNode,nodesPerRoute)
			data = loadOrRun(filename,calculateDubinPathResults,beta,radius,numberOfNode,nodesPerRoute)
			title = "{} Node Path".format(numberOfNode)
			filename = plot.path3(data["paths"],title)
			filenames.append(filename)
			titles.append(title)

		title = "UAV Routes and Paths through Latin Hypercubes".format(numberOfNode)
		uavRouteRef,uavRouteRefs = self.figures(filenames,title,titles)

		self.paragraph("Figure {} shows the optimal path and route for a UAV to circumnavigate a {} node Latin hypercube. The route is calculated before the path and then the path is calculated from the heading at each node in the route. From visual observation of the route it looks to be an optimal ordering of nodes and the path selected through the nodes adheres to the flight characteristics of a plane.".format(uavRouteRefs[0],numberOfNodes[0]))
		self.paragraph("Figure {} shows the optimal path and route for a UAV to circumnavigate a {} node Latin hypercube calculated in the same manner as the previous. Though this path is harder to visually inspect it looks to follow a path with limited change in height. In addition for each change in direction the flight characteristics are taken into account.".format(uavRouteRefs[1],numberOfNodes[0]))

	def energyModelResults(self):
		print("energyModelResults")

		if ("energyModelSectionRef" not in dir(self)):
			self.energyModelSectionRef  = None

		self.section("Energy Model Results","sub")
		self.paragraph("In section {} an energy model for the flight of a plane was defined. The varying coefficients of lift and drag were investigated to validate the iterative approach to define the Reynolds number. An example plane was selected to test whether the results for this model are viable. The energy coefficients of the plane considered defines the values taken forward in the report.".format(self.energyModelSectionRef))

		planeData = {
			r"Air Foil Name":					r"{}".format(planeEnergy.foilName),
			r"Mass $(kg)$":						r"$m = {:0.2f}$".format(planeEnergy.mass),
			r"Wing Span $(m)$":					r"$b = {:0.2f}$".format(planeEnergy.wingSpan),
			r"Wing Area $(m^2)$":				r"$S = {:0.3f}$".format(planeEnergy.wingArea),
			r"Oswald Factor":					r"$e = {:0.1f}$".format(planeEnergy.oswaldFactor)}
		calculatedPlaneData = {
			r"Aspect Ratio": 		r"${:0.2f}$".format(planeEnergy.wingSpan**2/planeEnergy.wingArea),
			r"Wing Chord $(m)$":	r"${:0.2f}$".format(planeEnergy.wingArea/planeEnergy.wingSpan)}

		planeTable = [[key,value] for key,value in sorted(planeData.items(),key=lambda x:x[0])]
		planeTableRef = self.table("Table of Plane Properties",planeTable,"l")
		self.paragraph("Table {} shows the properties of the plane considered. Aside from the name of the airfoil and the Oswald factor, all the parameters are readily available specifications that can be found on many out of the box UAVs. The airfoil was to be specified in order to obtain an estimation for the coefficients of lift and drag. The Oswald factor displayed in this table is also an estimation for the given plane; however for the purpose of this analysis is probably sufficient.".format(planeTableRef))

		calculatedPlaneTable = [[key,value] for key,value in sorted(calculatedPlaneData.items(),key=lambda x:x[0])]
		calculatedPlaneTableRef = self.table("Table of Calulated Plane Properties",calculatedPlaneTable,"l")
		self.paragraph(r"Table {} shows a number of calculated properties from the initial data. The aspect ratio was calculated using  $A = \frac{{b^2}}{{S}}$ and the wing chord was calculated using $c = \frac{{S}}{{b}}$. This allowes for any plane whose data can be fitted to the data in table {} to be used for this energy model.".format(calculatedPlaneTableRef,planeTableRef))
		self.paragraph(r"Given the main driving variable of analysis is the energy coefficient $\beta$, the energy coefficient output from the energy model was investigated. The flight velocity defines how great the drag force is that the plane works against in normal flight; therefore this was used as the driving variable to analyse the changing energy coefficient.")

		foilName,mass,wingSpan,wingArea,oswaldFactor,maxVelocity = planeEnergy.foilName,planeEnergy.mass,planeEnergy.wingSpan,planeEnergy.wingArea,planeEnergy.oswaldFactor,25
		filename = "calculations/energy_model_results_{}_{}_{}_{}_{}_{}.dat".format(foilName,mass,wingSpan,wingArea,oswaldFactor,maxVelocity)
		data = loadOrRun(filename,calculateEnergyModelResults,foilName,mass,wingSpan,wingArea,oswaldFactor,maxVelocity)

		title = r"Flight Velocity $V$ and Energy Coeficient $\beta$"
		scatter = {"Max Range":[[data["maxRangeVelocity"]],[data["maxRangeEnergyCoff"]]]}
		xLabel,yLabel =r"Flight Velocity $V (ms^{{-1}})$",r"Energy Coeficient $\beta$"
		filename = plot.path2(data["series"],title,xLabel=xLabel,yLabel=yLabel,scatter=scatter)
		energyCoffRef = self.figure(filename,title)

		self.paragraph("Figure {} shows the variation of the energy coefficient with flight velocity. The separate series define when the Reynolds number used to obtain the foil data has changed due to the velocity change. The Reynolds number can be plotted as a separate series as it is returned when the velocity of the plane is altered. For actual flight this curve would be a single line; however as the data sets are only available for certain Reynolds numbers the inconsistencies are present.".format(energyCoffRef))
		self.paragraph(r"The velocity that yields the greatest range given the plane considered is $V = {:0.1f} ms^{{-1}}$ at this flight velocity the energy coefficient takes the value $\beta = {:0.2f}$. For investigation of climbing and turning flight this is the flight velocity considered.".format(data["maxRangeVelocity"],data["maxRangeEnergyCoff"]))

		currentPlane = planeEnergy.PlaneEnergy(mass,wingSpan,wingArea,oswaldFactor)
		currentPlane.setAirFoil(foilName)
		currentPlane.setFlightVelocity(data["maxRangeVelocity"])
		angle,turnRadiuses = numpy.pi,numpy.linspace(1,100,100)
		distanceRadiuses = [(2*(turnRadiuses[-1]-turnRadius)+angle*turnRadius,turnRadius) for turnRadius in turnRadiuses]
		turnEnergyCosts = [currentPlane.turningFlight(distanceRadius[0],distanceRadius[1]) for distanceRadius in distanceRadiuses]
		angle = angle*180/numpy.pi

		title = r"Energy Cost of ${:0.0f}^{{\circ}}$ Turn at ${:0.1f} ms^{{-1}}$".format(angle,data["maxRangeVelocity"])
		xLabel,yLabel = r"Turn Radius $(m)$",r"Energy Cost $(m)$"
		filename = plot.line(turnRadiuses,turnEnergyCosts,title,xLabel,yLabel,tight=False)
		radiusCostRef = self.figure(filename,title,0.6)
		self.paragraph(r"Figure {} shows the variation in the cost of the plane detailed in table {} navigating a ${:0.0f}^{{\circ}}$ turn with varying turning radiuses. The varied turning radiuses cause the distance travelled to vary hugely. Thus if this analysis was only done with the circular distance of the turn, the cost would mainly be affected by this distance travelled. Therefore for this analysis the plane is assumed to start at one point, then, travel in a straight line until initiating a turn which passes through a second point half way round the turn before finishing the turn and flying back to be level with the initial point. This means as the turning radius is increased the straight line flight is decreased.".format(radiusCostRef,planeTableRef,angle))
		self.paragraph("It can be seen from figure {} that the energy consumed in turning ${:0.0f}^{{\circ}}$ reduces to an optimal at a given turning radius. This is due to the lesser forces required on the plane to turn with a greater turning circle. This finding needs to be considered when it comes to path planning.".format(radiusCostRef,angle))

		distance,climbHeights = 10,numpy.linspace(0,20,100)
		distanceHeights = [(numpy.sqrt(distance**2+climbHeight**2),climbHeight) for climbHeight in climbHeights]
		climbEnergyCosts = [currentPlane.climbingFlight(distanceHeight[0],distanceHeight[1]) for distanceHeight in distanceHeights]

		title = r"Energy Cost of Flight with Horizontal Distance ${:0.0f}m$ and Varyed Vertical Distance at ${:0.1f} ms^{{-1}}$".format(distance,data["maxRangeVelocity"])
		xLabel,yLabel = r"Climb Height $(m)$",r"Energy Cost $(m)$"
		filename = plot.line(climbHeights,climbEnergyCosts,title,xLabel,yLabel)
		radiusCostRef = self.figure(filename,title,0.6)
		self.paragraph(r"Figure {} shows the variation of the cost for the plane detailed in table {} to climb for a horizontal distance of ${:0.0f}m$ over varied climb heights. Here the horizontal distance is maintained at a constant and the vertical distance is increased to determine the extra flight cost. It can be seen that cost varies fairly linearly with climb height. This relationship is not truly accurate as it does not account for the reduction in aerodynamic efficiency which results from a greater angle of attack that is required for a greater climb angle. ".format(radiusCostRef,planeTableRef,distance))
		self.paragraph("The results to the energy model are as expected given the simplicity of the model utilised; however there is room for improvement on the accuracy of how the model predicts climbing and turning flight consumption. The framework for allowing any angle of attack to be pulled from the internet makes this improvement easy to facilitate.")

	def travellingPlaneResults(self):
		print("travellingPlaneResults")

		if ("progressiveSectionRef" not in dir(self)):
			self.progressiveSectionRef = None

		self.section("Progressive Travelling Plane","sub")
		self.paragraph("In section {} a best guess approach to the TSP was presented with specific application to the flight of a plane. This provided a method to calculate the order in which nodes should be visited for the lease cost route. The method was sufficiently computationally simple so that routes could be found through large numbers of nodes.".format(self.progressiveSectionRef))
		self.paragraph("To test the progressive algorithm fully the input parameters that affect its operation were varied to consider how they affected the resulting best guess cost. The following parameters affect the operation of the progressive travelling plane algorithm:")
		self.list([r"Number of nodes sample plan $N$",r"Number of nodes in subset $n$",r"Energy coefficient $\beta$"])
		self.paragraph("Before considering the quality of the model produced the parameters affecting the computation time were investigated. This allowed the further investigation of parameters to stay within reasonable limits. The energy coefficient does not change the computation time as the problem is the same complexity but it drastically changes the optimal ordering.")

		beta,numberOfNode,nodesPerRoutes = 0.1,10,[2,3,4,5]
		solutionLines = {}
		subsetResults = {"numberOfNode":[],"nodesPerRoute":nodesPerRoutes,"computeTime":[],"bestRoute":[],"bestCost":[]}
		for nodesPerRoute in nodesPerRoutes:
			filename = "calculations/progressive_route_results_{:0.1f}_{}_{}.dat".format(beta,numberOfNode,nodesPerRoute)
			data = loadOrRun(filename,calculateProgressiveResults,beta,numberOfNode,nodesPerRoute)
			subsetResults["numberOfNode"].append(numberOfNode)
			subsetResults["computeTime"].append(int(data["computeTime"]))
			subsetResults["bestRoute"].append(data["bestRoute"])
			subsetResults["bestCost"].append(data["bestCost"])
			solutionLines["{} Nodes".format(nodesPerRoute)]=data["bestCost"]
		subsetTableRef = self.table("Comparison of route calculation",[
			[r"Nodes in sample $N$"]+subsetResults["numberOfNode"],
			[r"Nodes in subset $n$"]+subsetResults["nodesPerRoute"],
			[r"Computation time $(ms)$"]+subsetResults["computeTime"],
			[r"Best route cost $(m)$"]+subsetResults["bestCost"]
			],"l")
		leastCost = min(subsetResults["bestCost"])
		leastCostNodes = subsetResults["nodesPerRoute"][subsetResults["bestCost"].index(leastCost)]

		self.paragraph("Table {} shows the effect of increasing the number of nodes considered in the subset, where subset refers to the number of nodes that are considered in each route of the progressive iteration of two routes. It is apparent that the computation time increases dramatically as seen in the exact TSP as the number of nodes in the subset is increased. This means computationally this method is not viable beyond {} nodes in each route in the subset.".format(subsetTableRef,nodesPerRoutes[-2]))
		
		beta,numberOfNodes,nodesPerRoute = 0.1,hypercubesConsidered,4
		sampleResults = {"numberOfNode":numberOfNodes,"nodesPerRoute":[],"computeTime":[],"bestRoute":[],"bestCost":[]}
		for numberOfNode in numberOfNodes:
			filename = "calculations/progressive_route_results_{:0.1f}_{}_{}.dat".format(beta,numberOfNode,nodesPerRoute)
			data = loadOrRun(filename,calculateProgressiveResults,beta,numberOfNode,nodesPerRoute)
			sampleResults["nodesPerRoute"].append(nodesPerRoute)
			sampleResults["computeTime"].append(int(data["computeTime"]))
			sampleResults["bestRoute"].append(data["bestRoute"])
			sampleResults["bestCost"].append(data["bestCost"])
		
		sampleTableRef = self.table("Comparison of route calculation",[
			[r"Nodes in sample $N$"]+sampleResults["numberOfNode"],
			[r"Nodes in subset $n$"]+sampleResults["nodesPerRoute"],
			[r"Computation time $(ms)$"]+sampleResults["computeTime"],
			[r"Best route cost $(m)$"]+sampleResults["bestCost"]
			],"l")

		self.paragraph("Table {} shows the effect of increasing the total number of nodes in the routing problem while maintaining the number of nodes in the subset at a constant. It can be seen that for {} nodes in the subset the computation time remains manageable as it did not increase drastically with greater numbers of nodes in the total sample.".format(sampleTableRef,numberOfNode))
		self.paragraph("The computation requirement of the progressive TSP is more than acceptable. However the routes produced may not be sufficiently close the actual optimum. Visual inspection of the given routes suggested that the logic is sound however the cost needs to be compared with the cost of the absolute optimal route. This is done by computing the costs of all routes using the exact TSP and then comparing.")
		
		numberOfNode = 10
		filename = "calculations/exact_route_results_cost_{:0.1f}_{}_{}.dat".format(beta,numberOfNode,True)
		data = loadOrRun(filename,calculateExactRouteResults,beta,numberOfNode,True)
		title = "Histogram of {} node route costs".format(numberOfNode)
		filename = plot.histogram(data["costs"],title,"Cost (m)","Frequency",solutionLines)
		histRef = self.figure(filename,title)
		self.paragraph("Figure {} shows a histogram of different route costs for a {} node Latin hypercube. The lines on this histogram plot represent the best cost routes with different numbers of nodes in the subset. It can be seen that the cost of the best route from the progressive approach closely approaches the optimal solution as calculated using the exact TSP.".format(histRef,numberOfNode,leastCostNodes))

		leastCostExact = min(data["costs"])
		leastCostPercentage = (leastCost-leastCostExact)/leastCostExact
		rankedCostDifference = [abs(item-leastCost) for item in sorted(data["costs"])]
		rankOfProgressive = rankedCostDifference.index(min(rankedCostDifference))
		totalResults = len(data["costs"])
		rankPercentage = rankOfProgressive/totalResults

		self.paragraph(r"The minimum cost route for the exact travelling plane was ${:0.2f}m$ while the minimum cost for the progressive travelling plane was ${:0.2f}m$; a figure is within ${:0.0%}$. In terms of ranking the best guess result ranks {:0.0f} out of {:0.0f} results. Which means the progressive best cost route is within ${:0.2%}$ of the rankings of all possible routes. Therefore for a {:0.0f} node route with the energy coefficient $\beta={:0.1f}$ the progressive travelling plane approach is very much acceptable.".format(leastCostExact,leastCost,leastCostPercentage,rankOfProgressive,totalResults,rankPercentage,numberOfNode,beta))
		self.paragraph("To fully test validity the progressive travelling plane route planner should have been compared with the exact results for Latin hypercubes with a number of nodes greater than {}; however the computation costs of a more than {} node routes makes this not a viable option. As an alternative, the relative cost decrease of adding more nodes can be considered.".format(numberOfNode,numberOfNode))
		
		beta,numberOfNodes,nodesPerRoutes = 0.1,hypercubesConsidered,[2,3,4,5]
		yAxis = {}
		for numberOfNode in numberOfNodes:
			yAxis["{} Nodes".format(numberOfNode)] = []
			for nodesPerRoute in nodesPerRoutes:
				filename = "calculations/progressive_route_results_{:0.1f}_{}_{}.dat".format(beta,numberOfNode,nodesPerRoute)
				data = loadOrRun(filename,calculateProgressiveResults,beta,numberOfNode,nodesPerRoute)
				yAxis["{} Nodes".format(numberOfNode)].append(data["bestCost"])
			currentSeries = yAxis["{} Nodes".format(numberOfNode)]
			yAxis["{} Nodes".format(numberOfNode)] = [item/min(currentSeries)*100 for item in currentSeries]

		title = "Comparison of Relative Route Costs for Progressive Travelling Plane"
		filename = plot.line(nodesPerRoutes,yAxis,title,xLabel=r"Nodes in subset $n$",yLabel=r"Cost Percentage $(\%)$",location=1)
		routeCostRef = self.figure(filename,title)

		self.paragraph("Figure {} shows how the relative route cost varies with the number of nodes in the subset. Relative route cost refers to the cost as a percentage of the minimum cost achieved. It has to be noted at this point that the minimum cost achieved is not the actual minimum cost route. However it does mean the relation of the other costs can be seen to the best computable cost and allows for comparison between vastly different numbers of nodes. From looking at this figure it can be seen that routes with less total nodes generally plateau within the range of the subset numbers investigated. This shows that the result achieved approaches some form of minimum. However, given the computational time to compute a route with {} node subsets is vast this is the furthest this analysis can be taken.".format(routeCostRef ,nodesPerRoute+1))
		self.paragraph(r"For the investigated energy coeficient $\beta = {}$ at low nodes the progressive TSP yields good results. However, given the energy coefficient $\beta$ depicts the relative cost of level vs inclined flight and that the progressive travelling planes is based on route planning through height order; changing this coefficient could have a big effect on the quality of the progressive approach.".format(beta))
		
		betas,numberOfNode,nodesPerRoute = ALL_BETAS,10,4
		yAxis = {r"Exact Cost $(m)$":[],r"Progressive Cost $(m)$":[]}
		for beta in betas:
			filename = "calculations/exact_route_results_cost_{:0.1f}_{}.dat".format(beta,numberOfNode)
			data = loadOrRun(filename,calculateExactRouteResults,beta,numberOfNode)
			yAxis[r"Exact Cost $(m)$"].append(data["bestCost"])
			filename = "calculations/progressive_route_results_{:0.1f}_{}_{}.dat".format(beta,numberOfNode,nodesPerRoute)
			data = loadOrRun(filename,calculateProgressiveResults,beta,numberOfNode,nodesPerRoute)
			yAxis[r"Progressive Cost $(m)$"].append(data["bestCost"])
		title = "Best Costs of Routes through {} Node Latin Hypercubes with Varying Energy Coeficients".format(numberOfNode)
		filename = plot.line(betas,yAxis,title,r"Energy Coeficient $\beta$",r"Route Cost $(m)$",location=2)
		energyCoffRef = self.figure(filename,title)

		self.paragraph(r"Figure {} shows how the progressive and exact travelling plane results are affected by changing the energy coefficient $\beta$. From looking at the results in this figure it can be seen that the progressive travelling plane approach holds true even when the energy coefficient is varied.".format(energyCoffRef))
		self.paragraph("The progressive travelling plane approach to route planning has been validated under varying parameters with links to the exact travelling plane model. An attempt has been made to verify that the quality of the results hold true for larger numbers of nodes however due to the inability to test this hypothesis directly this is not verified. The computational efficiency of the progressive TSP has been found to be far better than that of the exact TSP. As a result of these factors and given the extent of this analysis, the progressive TSP is acceptable to take forward to the next stage of the project.")

	def pathPlanningResults(self):
		print("pathPlanningResults")

		if ("pathPlanningSectionRef" not in dir(self)):
			self.pathPlanningSectionRef = None
		if ("energyModelSectionRef" not in dir(self)):
			self.energyModelSectionRef = None

		self.section("Path Planning","sub")
		self.paragraph("In section {} Dubins paths were utilised to produce navigable routes from a set of ordered nodes. The paths produced passed visual inspection of validity. The resulting effect on both path length and energy consumption are investigated to consider the importance of path planning for UAVs.".format(self.pathPlanningSectionRef))

		beta,nodesPerRoute,numberOfNodes = 0.1,4,[20,40,60,80,100,120]
		turnPercent = 0.1
		radiuses = numpy.linspace(0,turnPercent,5)
		xAxis,yAxis,lines = [],{},{}
		for radius in radiuses:
			yAxis["{:0.1%}".format(radius)]=[]
		for numberOfNode in numberOfNodes:
			pathDistances = []
			for radius in radiuses:
				filename = "calculations/dubin_path_results_{:0.1f}_{:0.3f}_{}_{}.dat".format(beta,radius,numberOfNode,nodesPerRoute)
				data = loadOrRun(filename,calculateDubinPathResults,beta,radius,numberOfNode,nodesPerRoute)
				pathDistance,routeDistance = data["pathDistance"],data["routeDistance"]
				pathDistances.append(pathDistance)
				yAxis["{:0.1%}".format(radius)].append(pathDistance)
			xAxis.append(routeDistance)
			lines["{} Nodes".format(numberOfNode)]=[(routeDistance,routeDistance),(min(pathDistances),max(pathDistances))]
		lines["Path = Route"]=[(min(xAxis),max(xAxis)),(min(xAxis),max(xAxis))]

		title = "Comparison of Path and Route Length for Varyed Nodes and Turning Radiuses"
		filename = (plot.scatter(xAxis,yAxis,title,xLabel="Route Length (m)",yLabel="Path Length (m)",lines=lines))
		pathRouteRef = self.figure(filename,title)

		self.paragraph("Figure {} shows the relationship between the route length and path length for a number of different Latin hypercubes. For each Latin hypercube the distance of the shortest route (length of ordered route through nodes) and a number of shortest paths (length of path through ordered nodes that takes into account the flight characteristics of the plane) have been calculated and compared. The shortest paths are considered with turning radiuses varied between ${:0.0%}$ and ${:0.0%}$ of the length of the side of the area that is being explored. For this analysis the area of interest is a unit cube and the percentage value represents the maximum turning radius of the plane over the length of one axis.".format(pathRouteRef,0,turnPercent))

		self.paragraph("It can be seen from figure {} that as the number of nodes in the Latin hypercube is increased (vertical coloured lines indicate a set of tests on a single Latin hypercube) the effect of increased turning radius (turning radius is indicated by sets of coloured points) also increases. For the case where the turning radius is $0%$ the path length and route length are the same as the UAV can affectively turn on the spot. Given the size of the research area that will be utilised for collecting atmospheric data using a UAV the added distance due to path length will have a negligible effect on the final distance. The stage at which this consideration may be required to be considered is in computing the final energy of the path. This is due to the greater accuracy of energy cost being required at this stage.".format(pathRouteRef))
		self.paragraph("To utilise the path planning component in computing a best estimation of the energy consumed along the path, the energy as a result of turning radius needs to be considered along with that of level and turning flight. The energy consumed in a turn is a result of the severity of the turn and the distance travelled in that turn. The energy model presented in section {} was able to compute the energy cost of navigating a turn at a given radius. The energy consumed was found to have an optimal value where the balance between high force turning angle and long distance turning against drag were at a minimum. For the path planning problem the effect of the turning radius must be considered.".format(self.energyModelSectionRef))

		numberOfNode,maxTurnRadius,flightVelocity = 20,20,10
		filename = "calculations/dubin_energy_results_{}_{:0.0f}_{:0.0f}.dat".format(numberOfNode,maxTurnRadius,flightVelocity)
		data = loadOrRun(filename,calculateDubinEnergyResults,numberOfNode,maxTurnRadius,flightVelocity)
		turnRadiuses = data["turnRadius"][1:]
		pathEnergys = data["pathEnergy"][1:]

		title = "Total Path Energy for Route through {} Node Latin Hypercube with Changing Turning Radius".format(numberOfNode)
		filename = plot.line(turnRadiuses,pathEnergys,title,"Turning Radius $(m)$","Total Energy $(J)$",location=2,tight=False)
		pathEnergyRef = self.figure(filename,title)

		energyRangePercentage = (max(pathEnergys)-min(pathEnergys))/min(pathEnergys)
		self.paragraph("Figure {} shows the variation of path energy through a {} node Latin hypercube at {}m/s as a result of altered turning radius. It can be seen that the turning radius affects the total energy consumed on the route and has an optimal value. This optimal value is a product of the spacing of the nodes in the sample plan and the velocity of the plane. The variation in energy as a percentage of the minimum energy experienced is only {:0.2%} therefore the variation of turning radius on the energy cost is sufficiently negligible to disregard.".format(pathEnergyRef,numberOfNode,flightVelocity,energyRangePercentage))

		numberOfNodes,maxTurnRadius,flightVelocity = [18,20,22],20,10
		yAxis = {}
		for numberOfNode in numberOfNodes:
			filename = "calculations/dubin_energy_results_{}_{:0.0f}_{:0.0f}.dat".format(numberOfNode,maxTurnRadius,flightVelocity)
			data = loadOrRun(filename,calculateDubinEnergyResults,numberOfNode,maxTurnRadius,flightVelocity)
			turnRadiuses = data["turnRadius"]
			pathEnergys = data["pathEnergy"]
			yAxis["{} Nodes".format(numberOfNode)] = [100*pathEnergy/pathEnergys[1] for pathEnergy in pathEnergys]

		title = "Percentage Path Energy for Routes through a Number of Node Latin Hypercubes with Changing Turning Radius".format(numberOfNode)
		filename = plot.line(turnRadiuses,yAxis,title,"Turning Radius $(m)$",r"Energy Percentage $(\%)$",location=2,tight=False)
		pathNodesEnergyRef = self.figure(filename,title)
		self.paragraph("Figure {} shows the variation of the path energy as a result of varied turning radiuses and number of nodes in the sample plan. This figure is to illustrate the effect of node spacing on the energy consumption of a path. The Latin hypercubes with greater numbers of nodes have closer packed nodes therefore the lower turning radiuses are more optimal. The percentage change to the energy of the route is negligible as a result of increase turning radius however this is purely illustrative of the effect of node spacing. The energy percentage here is the energy as a percentage value of the energy required for a route with a turning radius of unity.".format(pathNodesEnergyRef))

		flightVelocities = numpy.linspace(8,16,5)
		yAxis,pathEnergy = {},{}
		for flightVelocity in flightVelocities:
			filename = "calculations/dubin_energy_results_{}_{:0.0f}_{:0.0f}.dat".format(numberOfNode,maxTurnRadius,flightVelocity)
			data = loadOrRun(filename,calculateDubinEnergyResults,numberOfNode,maxTurnRadius,flightVelocity)
			turnRadiuses = data["turnRadius"]
			pathEnergys = data["pathEnergy"]
                        #print(type(pathEnergy))
                        #print(pathEnergy)
			pathEnergy[str(flightVelocity)] = pathEnergys
                        #print(type(pathEnergy))
			yAxis["{} m/s".format(flightVelocity)] = [100*item/pathEnergys[1] for item in pathEnergys]
		title = "Percentage Path Energy for Route through {} Node Latin Hypercube with Changing Turning Radius and Flight Velocity".format(numberOfNode)
		filename = plot.line(turnRadiuses,yAxis,title,"Turning Radius $(m)$",r"Energy Percentage $(\%)$",location=2,tight=False)
		pathVelocityEnergyRef = self.figure(filename,title)
		self.paragraph("Figure {} shows the variation of total path energy as a result of varied turning radiuses and flight velocities. This figure is to illustrate the effect of flight velocity on the energy consumption of a path. The energy percentage here is the energy as a percentage value of the energy required for a route with a turning radius of unity. It can be seen that the greater the flight velocity the higher the optimal turning radius is. This figure displays percentage values as the energy increases drastically given greater flight velocities.".format(pathVelocityEnergyRef))
		self.paragraph("The path planing component of this report allows the energy consumed by a UAV in navigating a sample plan to be more accurately calculated as the effect of the turning radius can be investigated. This means the path to be optimised for the best turning radius given a route. Additionally the findings outline the potential for the turning radius to be optimised for least energy consumed based on a node by node basis, this suggestion is due to the optimal turning radius being dependent on node spacing therefore should be calculated per node as the distance between each node is very different. For the continuation of this project the added energy consumption due to the UAV flight path will be disregarded as the energy consumption is not vastly different to that of the route for large turning radiuses in comparison to the research area.")

	def modelResults(self):
		print("modelResults")

		self.section("Sample Plan Model","sub")
		beta,numberNode,testCases,maxLength = 0.1,100,100,1000

		self.paragraph("Thus far in the report routes have been found from a collection of nodes in particular sampling plans, the number of nodes in the sampling plan along with the area of interest affects the length of the route through the points and the total height change experienced. These two factors then go to calculating the total energy expenditure of the route. The desired design route is to calculate the desired route given the area of interest and total energy of the plane. This requires the relationship between the length, width and height of the research area and the number of nodes in the sample plan to the resulting energy cost of the route to be modelled.")
		self.paragraph("The problem with computing this relationship is that the route through the sample area is dependent upon the energy model for a given plane. As in the extremes the energy model can completely favour either climbing flight or level flight.") 
		self.paragraph("To compute a model for each Latin hypercube a sampling plan was defined with {} test cases this sampling plan ranged between 0 and {} in each vertex. These sampling plans provide for the most efficient way to collect data on each Latin hypercube. For each Latin hypercube with between {} and {} nodes all test cases are analysed to return the exact energy cost. This energy cost can then be related to the research volume for each set of node numbers.".format(testCases,maxLength,ALL_NODES[0],ALL_NODES[-1]))

		sampleDiagramRef = self.figure("figures/data_model_diagram.png","Diagram of Sample Plan Model Logic",1)
		self.paragraph("Figure {} shows the logic required to plan a route based on the total energy available. In this diagram the calculation of model variables is shown in the process. However if these variables were required to be calculated on the fly this would not be a viable approach. In addition if this were to be calculated each and every time the exact research area would be used for each number of nodes, as opposed to 100 samples which are used to return a model for the varying route cost given a number of nodes.".format(sampleDiagramRef))

		data = buildModel.computeResults(beta,numberNode)
		energyParameters = buildModel.returnModel(beta,numberNode)
		x,y,z,e = numpy.array([data["X"],data["Y"],data["Z"],data["Energy"]])

		title = "Scatter plot of varying route and path lengths for a {} node Latin hypercube model".format(numberNode)
		xLabel,yLabel,zLabel = r"Research Area [$X \times Y$](m^2)","Reseach Height (m)","Route Cost (m)"
		zAxis = {"Actual":e,"Predicted":buildModel.energyModel(energyParameters,x,y,z)}
		filename = plot.scatter3(x*y,z,zAxis,title,xLabel=xLabel,yLabel=yLabel,zLabel=zLabel)
		energyFigRef = self.figure(filename,title)

		self.paragraph("Figure {} shows the relationship between the research area ($x \times y$), research height ($z$) and the resulting route cost. This depicts that the energy required to circumnavigate a {} node Latin hypercube, varies non linearly with both the area and height. This figure shows that the model needs to be computed from both the length and width as opposed to the area however this form allows for depiction on a figure.".format(energyFigRef,numberNode))
		energyEqRef = self.equation("Energy Equation",buildModel.getEquation())
		self.paragraph("Equation {} shows the format of how the length, width and height of the research area affect the route cost. For every number of node, Latin hypercube and energy coefficients different model parameters are required to correctly depict the relation between the dimension inputs and the energy cost.".format(energyEqRef))
		energyNumEqRef = self.equation("{} Node Energy Equation".format(numberNode),buildModel.getEquation(beta,numberNode))
		self.paragraph("Equation {} shows how the length, width and height of the research area affects the route energy for a route determined by the energy coefficient {} through a {} node Latin hypercube. The parameters here are calculated using a least squares regression function.".format(energyNumEqRef,beta,numberNode))
		self.paragraph("To calcualte the actual route energy from this cost the energy factor gamma is required. The route cost can simply be multiplied by gamma for the plane considered for routing and this model produces the total route cost for a particular plane without having to compute all costs of routing round different Latin hypercubes.")

		maxLength,maxEnergy,betas = 1000,2000,ALL_BETAS

		beta = betas[0]
		filename = "calculations/model_results_{:0.1f}_{:0.0f}_{:0.0f}.dat".format(beta,maxLength,maxEnergy)
		data = loadOrRun(filename,testModelResults,beta,maxLength,maxEnergy)
		series,predictionErrors = data["series"],data["predictionError"]
		lines = {"Perfect Prediction":[[0,maxEnergy],[0,maxEnergy]]}
		title = r"Energy Model Prediction Compared with Calculated Energies For Energy Coeficient $\beta = {:0.1f}$".format(beta)
		filename = plot.scatter2(series,title,xLabel="Desired Energy (J)",yLabel="Actual Energy (J)",lines=lines,location=2)
		predictedActualRef = self.figure(filename,title,0.9)
		self.paragraph(r"Figure {} shows the comparison of the desired route energy and the resulting route energy for the energy coefficient $\beta = {:0.1f}$. The inclined line through the data shows the optimal result where the prediction is completely accurate. This data is obtained from randomly varying the research area and the desired energy consumption and then computing the number of nodes that are predicted to make up the route that is optimal. The actual energy of this route is then calculated exactly and plotted in comparison to the desired route. The series represent the number of nodes used to produce the routes.".format(predictedActualRef,beta))
		averagePredictionError = sum(predictionErrors)/len(predictionErrors)
		stdDevPredictionError= numpy.std(predictionErrors)
		self.paragraph(r"The predictions seen for the case where $\beta={}$ are on average out by {:0.2%} of the desired route energy. This suggests that for this energy coefficient the model produced is viable to accurately select a sampling plan given a required energy consumption. This may not be the case for other energy coefficients due to the drastic affect the energy coefficient has on the routing problem.".format(beta,averagePredictionError))

		filenames,titles,averagePredictionErrors,stdDevPredictionErrors = [],[],[averagePredictionError],[stdDevPredictionError]
		for beta in betas[1:]:
			filename = "calculations/model_results_{:0.1f}_{:0.0f}_{:0.0f}.dat".format(beta,maxLength,maxEnergy)
			data = loadOrRun(filename,testModelResults,beta,maxLength,maxEnergy)
			series,predictionErrors = data["series"],data["predictionError"]
			lines = {"Perfect Prediction":[[0,maxEnergy],[0,maxEnergy]]}
			title = r"$\beta = {:0.1f}$".format(beta)
			filename = plot.scatter2(series,title,xLabel="Desired Energy (J)",yLabel="Actual Energy (J)",lines=lines,location=2)
			filenames.append(filename)
			titles.append(title)
			averagePredictionErrors.append(sum(predictionErrors)/len(predictionErrors))
			stdDevPredictionErrors.append(numpy.std(predictionErrors))
		title = r"Energy Model Prediction Compared with Calculated Energies For Varying Energy Coeficients $\beta$"
		predictedActualRef2,predictedActualRefs = self.figures(filenames,title,titles)
		predictedActualRefs.insert(0,predictedActualRef)
		self.paragraph(r"Figure {} shows the comparison of desired and actual route energies for random sample areas and desired route energies for the energy coefficients $\beta =$ {}, {} and {}. It can be seen that as the energy coefficient is increased the prediction accuracy for the route becomes less viable. Given these predictions are for specific values of the energy coefficient these results would get less accurate given any value for the energy coefficient being utilised. This would be the case for real implementation as the value for the energy coefficient is precisely defined from the plane energy model.".format(predictedActualRef2,betas[-3],betas[-2],betas[-1]))

		table = [[predictedActualRefs[i],r"${}$".format(betas[i]),"{:0.2%}".format(averagePredictionErrors[i]),"{:0.2%}".format(stdDevPredictionErrors[i])] for i in range(len(predictedActualRefs))]
		table.insert(0,["Figure",r"Energy Coeficient $(\beta)$","Prediction Error","Prediction Standard Deviation"])
		resultsTable = self.table("Table of Results",table)
		self.paragraph("Table {} shows the prediction error variation as a result of varying the value of the energy coefficient. It can be seen that the model predictions are only viable for low values of the energy coefficient. Therefore the model is of an acceptable accuracy to be utilised in the model predictions for low values of the energy coefficient. Given the UAV considered in this report has a low energy coefficient at optimal range velocity this suggests that this model would be acceptable for use within path planning for the purpose of collecting atmospheric data using UAVs, as this enables a research area to be specified and a suitable Latin hypercube to be selected given the desired total energy expenditure.".format(resultsTable))

	def conclusions(self):
		print("conclusions")
		self.paragraph("This report has looked at collection of atmospheric data using UAVs with specific focus on collecting the best set of sample data for a given research area while maximising utlisation of the energy contained within the plane. To complete this task Latin hypercubes were used to provide optimal space filling sampling plans and then the least cost route, with the path then calculated through the Latin hypercubes. To enable planning from the basis of the required energy consumption, the plane's energy consumption was modelled in a mannar where a single coefficient defines the route characteristics. This enabled a model to be produced from multiple tests that can predict the energy consumed based on the number of nodes in the Latin hypercube. This provides for the best spread of data collection and adheres to the UAV energy requirement.")
		self.section("Energy Model","sub")
		self.paragraph("The energy model produced uses the most simplified aerodynamic equations to determine the cost of navigating a certain path. Given the simplicity of the energy model, routing can be characterised based on a single variable which can be used in a sample model that determines the optimal number of nodes. The coefficients of lift and drag selected for the plane do not accurately portray the real values that will be experienced as they are pulled for purely the airfoil in question. For the routing component of this project the ranking of energy cost is taken to be more important than actual cost this is acceptable. However the drag effects of the plane fuselage need to be accounted for otherwise a route calculated would far exceed the predicted energy. The values utilised for the air density and viscosity in this model assume that they remain constant at all altitudes in the research area which is not an accurate assumption when altitude varied greatly.")
		self.section("Travelling Plane","sub")
		self.paragraph("The progressive approach to the TSP yields a good estimation as to the least cost path to navigate a number of nodes. This enables route planning with numbers of nodes that would not be possible using the exact travelling salesman. Therefore the calculation produced is of significant value. The limitation lies in how many nodes the planning can be relied upon to route though while maintaining a best guess cost. Due to the inability to collect data on the perfect solution for more than 10 nodes I have found no sound method for substantiating routing though a {} node hypercube. The quality of results obtained in the tests performed suggested this route logic to be solid for what has been tested though. This approach provides what it set out to accomplish which is a best guess solution to route planning that is sufficient to be confident of this routing algorithm for the basis of the subsequent calculations".format(hypercubesConsidered[-1]))
		self.section("Path Planning","sub")
		self.paragraph("Utilising Dubins paths to take into account the flight characteristics of the plane enables the energy model to be applied more accurately and the turning radius to be optimised according to the increased consumption related to the bank angle of the turn. Dubins paths are well documented solutions to the problem of vehicle paths and there has been previous literature on applying them in three dimensions. Therefore the shortest distance paths calculated in this report are likely to be correct as any issues can be visually defined. However in light of analysis the shortest Dubins paths do not always correspond to the least energy path due to the increased energy required for a smaller turning radius. Working to improve the implementation of these paths is important as this project strives to compute an as accurate as possible energy cost.")
		self.section("Data Model","sub")
		self.paragraph("The data model calculated works well for low values of the energy consumption coefficient that directly correspond to the energy coefficient used to produce the model. However for higher values of the coefficient or in-between two tests where there is a lack of data from previous tests the model is not accurate enough for utilisation. With enough test cases where the energy coefficient is varied using a four dimension sampling plan not just the three dimensions which define the area of interest, the model produced is likely to hold sufficient worth to confidently predict costs for any low energy coefficient, not just coefficients that lie in previously tested conditions. The correlations of the sample model are only viable in the confines of the current energy model therefore an improvement on the energy model would require updating the sample model to reflect the added complexity.")
		self.section("Looking Forward","sub")
		self.paragraph("The approaches documented here are far from a perfect approach to the problem of collecting atmospheric data. However the combination of sampling plans and the progressive travelling plane approach to path planning for atmospheric data collection presents an interesting foothold for further investigation. In addition the proof that, in its simplest form a model can be produced that allows planning from the basis of the required energy consumption, facilitates the potential (however small) for this work to be utilised in actual path planning for atmospheric data collection.")
		self.paragraph("An initial aim of the project was to include consideration for uniform wind which would make the path planning presented here closer to the optimal. Dubins paths in the wind frame of reference correspond to trichordial path segments in the ground frame of reference. This would require a further geometrical calculation to enable this consideration to the path planing. In terms of the routing problem a previous energy model for this project included the consideration on computing the line integral through a vector field that allowed the distance of travel to be altered for the prevailing wind. This means that the cost of travel from nodes could be altered to consider even a non-uniform wind, however was not included for the final report due to the complexities of implementation.")
		self.paragraph("Given the energy model is the basis for all routing consideration in this project, a non-linear approach to energy modelling would have the facility to correctly ascertain the cost of not just changing height but consider the rate at which the rate of height change can occur. But such non-linear version of the energy model would not be viable in the route planning stage as the cost of travel between nodes is considered as individual components. However upon calculation of the path, a non-linear energy model could provide a far more accurate method to defining the exact energy required by a UAV.")

	def projectPlan(self):
		print("projectPlan")
		self.section("Project Management and Organisation","sub")
		self.paragraph("To complete the objectives of this project while allowing sufficient time for each step careful project management was required. To produce a project plan the objectives of the project were considered and broken down into the elements that were required to complete each stage. The prerequisite requirements of each item in the project plan were then defined to ensure that each step could be completed when required. These requirements led to a framework for a project plan that only required estimation of the time required for each stage to be complete.")
		projectPlanRef = self.figure("figures/project_plan.png","Gantt Chart of Project Plan",0.8,"[H]")
		self.paragraph("Figure {} shows the project plan followed.  The steps are on the left and the time which is allocated for completion indicated by coloured squares. This plan was not followed to the letter as some of the stages were more complicated than first imagined so a more gradual approach to developing the solution was required. These overruns were either due to more detailed literature analysis being required or continued trial and error on the part of programming the solution.".format(projectPlanRef))

	def documentWriting(self):
		print("documentWriting")
		self.section("Writing the Report","sub")
		self.paragraph("The consideration and thought that went into composing ideas in the report often led to further analysis on the part of the code produced, it therefore seemed logical to produce the report in a more adaptive manor. This resulted in designing a parametric report where calculations, results and figures were automatically updated upon each run.")
		self.paragraph("The adaptive report is written in python as all other project elements were computed using python. The basis of the logic is a TexDocument class that has a number of methods that deal with adding basic elements to a LaTeX document. Within the main content document these methods can easily be called to define: sections, paragraphs, figures, equations and tables. All these elements are added to a working LaTeX document as they are interpreted. Upon completion of the report the compile method can be called which calls pdfTex and BibLaTeX to build the pdf and automatically open it to view. In addition to standard features this approach means that: the LaTeX document automatically remunerates figure labels if there is repetition to ensure there is no cross over and nomeclature and abreviations can be collected within a dictionary from any point within the report.")
		self.paragraph("Producing the report in this way means that whatever change of code was made can easily result in an updated report. The drawback however is the compute time required to compile the report. This problem was levitated using cached results to computations. The function loadOrRun within the shared module of the code for this project deals with caching of results. If parameters are changes then the cache automatically recalculates the required data. Additionally all display logic is run on each compile so a change in plot style is quick and easy to implement without having to recomputed the cache.")
		
	def pythonCode(self):
		print("pythonCode")
		self.section("Python Code")
		self.paragraph("To use the functionality of this code the scipy stack is required. To enable writing of LaTeX files MikTex needs to be installed. If further Latin hypercubes need to be calculated MATLAB needs to run on the system. Calls to MikTex and MATLAB are wrtten on a windows computere so the cammand line calls are in windows syntax.")
		self.paragraph("The python code included within the CD has the following modules:")
		# self.list(["Shared","Plane Energy","Air Foil","Latin Hypercube","Travelling Plane","Sample Model","Dubins Path"])
		self.paragraph(r"\textbf{Shared} is a module that contains all the logic available that is required by all modules of the project and contains generic functions that could be used in all locations.")
		self.paragraph(r"\textbf{Plane energy} is a module that is used to model the energy consumption of a plane. This module contains a number of global variables that define a default plane. A single class within this module is constructed using plane variables, this class is capable of computing the energy required for a number of flight manoeuvres and returning the energy coefficient and energy factor.")
		self.paragraph(r"\textbf{Airfoil} is a module that is used to obtain data on a number of airfoils using \textit{airfoiltools.com}. The class contained within this module is constructed with a foil name and Reynolds number and can return the variation of the lift and drag coefficients with changing angle of attack.")
		self.paragraph(r"\textbf{Latin hypercube} is a module that calls MATLAB to connect with the code produced by \citen{Forrester2008} and return Latin hypercube sampling plans of any given number of nodes and number of dimensions. The results to these MATLAB calls are cached to reduce the time of subsequent calls.")
		self.paragraph(r"\textbf{Travelling plane} is a module that is used to calculate the least cost route through given nodes. The module contains both the exact all routes approach and the progressive travelling plane approach.")
		self.paragraph(r"\textbf{Sample model} is a module that is used to compute models of the energy cost of a routes given different scenarios. This module enables the route planning for atmospheric data collection to be done from the requirement of total energy consumed.")
		self.paragraph(r"\textbf{Dubins path} is a module used to compute the shortest distance Dubins paths either between two points with start and end directions defined or using the Dubins Path class the total path through a number of nodes. This module is not fully commented as the geometric logic is from \citen{Giese2012} and there is a lot of lines of code to explain.")
