from itertools import permutations

nodes= "0123"

for item in permutations(nodes,len(nodes)):
	print(item)

results = [[int(index) for index in route] for route in permutations(nodes,len(nodes))]

print(results)