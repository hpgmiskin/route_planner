#Code to compile the report
from shared import *
from texDocument import TexDocument
import travellingPlane,dubinPath,plot

print("Plane Properties")
#TODO
print("Energy Model")
#TODO
print("Latin Hypercubes")

hypercubes = [10,50,250,1250]
for hypercube in hypercubes:
	nodes = latinHypercube(hypercube)
	[x,y,z] = changeArray(nodes)
	plot.plotScatter3(x,y,z,"Nodes {}".format(hypercube))


