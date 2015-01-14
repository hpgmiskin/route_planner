#route_planner

Route planner is a collection of python functions which support my individual project. The aim of this project was to design an optimal route for a unmanned aerial vehicle, this was achieved by using an incarnation of the travelling salesman problem. I altered the standard travelling salesman problem so that the length of the vertexes were  considered as the energy cost of flying between the two.This results in a travelling salesman problem that cant be solved using existing heuristics as the weight of the vertex is not the euclidean distance.

##Contents

###Shared
Contains all the logic available that is required by all modules of the project and contains generic functions that could be used in all locations.  

###Plane Energy
Used to model the energy consumption of a plane. This module contains a number of global variables that define a default plane. A single class within this module is constructed using plane variables, this class is capable of computing the energy required for a number of flight manoeuvres and returning the energy coefficient and energy factor.

###Air Foil
Used to obtain data on a number of airfoils using airfoil-tools.com. The class contained within this module is constructed with a foil name and Reynolds number and can return the variation of the lift and drag coefficients with changing angle of attack.

###Latin Hypercube
Calls MATLAB to connect with the code produced by Forrester et al and return Latin hypercube sampling plans of any given number of nodes and number of dimensions. The results to these MATLAB calls are cached to reduce the time of subsequent calls.  

###Travelling Plane
Used to calculate the least cost route through given nodes. The module contains both the exact all routes approach and the progressive travelling plane approach.  

###Sample Model
Used to compute models of the energy cost of a routes given different scenarios. This module enables the route planning for atmospheric data collection to be done from the requirement of total energy consumed.  

###Dubin's Path
Used to compute the shortest distance Dubins paths either between two points with start and end directions defined or using the Dubins Path class the total path through a number of nodes. This module is not fully commented as the geometric logic is from Giese and there is a lot of lines of code to explain. 

##Licence
Please feel free to use any pieces of code so long as it is for personal use and credit is given where code is directly copied.