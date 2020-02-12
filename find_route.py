# Alvin Poudel Sharma
#1001555230

import sys
from queue import PriorityQueue


# class for a node that has the ciy name cumulative cost node level and its parent

class node:
	def __init__(self, parent , city , c_cost , n_level):
		self.parent = parent
		self.city = city
		self.c_cost = c_cost
		self.n_level = n_level

#--------------------------------------------------

# this functions has current node, fringe, ravelled set , data table
# heuristic table and trackers for node generated and boolean to 
#check if heuristic is to use or not.
# the function expands the current node and adds it to the fringe by checking if it has been travelled or not
# returns the count of generated node
def expand_node(current,fringe,travelled, table, heuristic , node_generated, use_heuristic):

	possibility = table[current.city]
	
	for child in possibility:
		node_generated += 1
		if( child not in travelled):
			child_node = node(current,child, current.c_cost+ int(possibility[child]) , current.n_level+ 1 ) 
			
			if use_heuristic ==False:
				fringe.put((current.c_cost+ int(possibility[child]), id(child_node ),child_node))
			else:
				fringe.put((heuristic[child]+ current.c_cost+ int(possibility[child]), id(child_node ),child_node))


	return node_generated

#--------------------------------------------------

# function that has parameters that are data table, start and end state and heuristic value 
# has various trackers to track the node generated and max memory used by the fringe 
# generates root node and gets a node from the queue and adds to the travelled set if not added before
#returns the solution if found else reture None.

def graph_search(table , start , goal , heuristic):

	node_expanded = 0
	node_generated = 0
	max_node_in_mem =0;
	use_heuristic = False
	if len(heuristic) !=0:
		use_heuristic = True


	travelled = []
	fringe = PriorityQueue()
	current_level = 0 
	root = node(None, start , 0, 0)
	node_generated += 1 
	if use_heuristic ==False:
		fringe.put((0,id(root),root))
	else:
		fringe.put((0+ heuristic[start] ,id(root),root))

	while not fringe.empty():

		if max_node_in_mem < fringe.qsize():
			max_node_in_mem = fringe.qsize()

		current = fringe.get()[2]
	
		if (current.city == goal ):
			return node_expanded , node_generated , max_node_in_mem , current
		
		if( current.city not in travelled):
			travelled.append(current.city)
			node_generated = expand_node(current,fringe,travelled, table, heuristic, node_generated, use_heuristic)
			node_expanded += 1


	return node_expanded , node_generated , max_node_in_mem , None

#--------------------------------------------------
# helper functions that prints the solution obtained using recursion.
# takes solution node as the parameter.
def print_sol(solution):

	if solution.parent == None:
		return

	print_sol(solution.parent)
	print("%s to %s, %.2f km" % ((solution.parent).city ,solution.city, solution.c_cost- (solution.parent).c_cost ))

	return

#--------------------------------------------------

# a helper function that has data table , start and goal state and heuristic provided by the user.
# calls graph search for finding solution to our problem.

def find_route(table , start , goal , heuristic):

	
	node_expanded , node_generated, max_node_in_mem , solution = graph_search(table , start , goal , heuristic) 

	print('')
	print("nodes expanded:%3d" %(node_expanded))
	print("nodes generated:%2d" %(node_generated))
	print("max nodes in memory:%2d" %(max_node_in_mem))
	if(solution == None ):
		print('distance: infinity')
		print("route:")
		print("none")
	else:
		print("distance: %.2f km" % (solution.c_cost))
		print("route:")
		print_sol(solution)





	return

#--------------------------------------------------

# reads the heuristic data from a file and stores in a dictionary
def heuristic_reader(filename):

	heuristic = {}

	with open( filename, 'r' ) as fp :
		lines = fp.read().replace( '\r', '' ).split( '\n' )
	
	for line in lines :
			if line == "END OF INPUT" :
				break
			temp = line.split()

			heuristic[temp[0]] = temp[1];

	return heuristic


#--------------------------------------------------

# reads the city map and stores it in a dictionary of a dictinary for a fast lookup
def table_creator( filename ):
	table = {}

	with open( filename, 'r' ) as fp :
		lines = fp.read().replace( '\r', '' ).split( '\n' )
	
	for line in lines :
			if line == "END OF INPUT" :
				break
			temp = line.split()

			if temp[0] in table:
				(table[temp[0]])[temp[1]] = temp[2]
			else:
				path1 = {}
				path1[temp[1]] = temp[2]
				table[temp[0]] = path1;

			if temp[1] in table:
				(table[temp[1]])[temp[0]] = temp[2]
			else:							
				path2 = {}
				path2[temp[0]] = temp[2]
				table[temp[1]] = path2;
				

	return table

#--------------------------------------------------
# main function that takes commandline argv and opens respective files and store it in the data structure.
def main() :
	
	table ={}
	heuristic = {}

	if len(sys.argv) < 4 :
		print("##Invalid input.")
		return

	table = table_creator(sys.argv[1])

	start = sys.argv[2]
	goal = sys.argv[3]
	
	if(len(sys.argv)== 5):
		heuristic = heuristic_reader(sys.argv[4])
	
	find_route(table, start , goal , heuristic)

#--------------------------------------------------

if ( __name__ == '__main__' ) :
	main()

#--------------------------------------------------