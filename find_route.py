import sys
from queue import PriorityQueue

class node:
	def __init__(self, parent , city , c_cost , n_level):
		self.parent = parent
		self.city = city
		self.c_cost = c_cost
		self.n_level = n_level

#--------------------------------------------------

def expand_node(current,fringe,travelled, table, heuristic , node_generated):

	possibility = table[current.city]
	
	for child in possibility:
		if( child not in travelled):
			node_generated += 1
			fringe.put((current.c_cost+ int(possibility[child]), node(current,child, current.c_cost+ int(possibility[child]) , current.n_level+ 1 ) ))

	return 

#--------------------------------------------------

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
	fringe.put((0,root))
	i =0
	while not fringe.empty():

		if max_node_in_mem < fringe.qsize():
			max_node_in_mem = fringe.qsize()

		current = fringe.get()[1]
		print('Node cost is ' + str(i) )
		print(current.c_cost)
		i+=1
		if (current.city == goal ):
			return node_expanded , node_generated , max_node_in_mem , current
		
		if( current.city not in travelled):
			travelled.append(current.city)
			expand_node(current,fringe,travelled, table, heuristic, node_generated)
			node_expanded += 1


	return node_expanded , node_generated , max_node_in_mem , None

#--------------------------------------------------

def find_route(table , start , goal , heuristic):

	
	node_expanded , node_generated, max_node_in_mem , solution = graph_search(table , start , goal , heuristic) 


	print('nodes expanded : '+ str(node_expanded))
	print('nodes generated: '+ str(node_generated))
	print('max nodes in memory: '+ str(max_node_in_mem))
	if(solution == None ):
		print('distance : infinity')
	else:
		print('distance :'+ str(solution.c_cost))
		print('level :'+ str(solution.n_level))






	return

#--------------------------------------------------

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

def main() :
	
	table ={}
	heuristic = {}

	if len(sys.argv) < 4 :
		print("##Invalid input.")
		return

	table = table_creator(sys.argv[1])

	for x in table:
		print(x + ' ->> ' + str(table[x]))


	
	start = sys.argv[2]
	goal = sys.argv[3]
	
	if(len(sys.argv)== 5):
		heuristic = heuristic_reader(sys.argv[4])
	
	find_route(table, start , goal , heuristic)

#--------------------------------------------------

if ( __name__ == '__main__' ) :
	main()

#--------------------------------------------------