# def minimumTime(numOfParts, parts):
#     # WRITE YOUR CODE HERE
#     # Sort the parts list
#     sorted_parts = sorted(parts)
#     print(sorted_parts)
#     merged_parts = []
#     items = 1
#     merged_num = sorted_parts[0]
#     while items < numOfParts:
#         merged_num = merged_num + sorted_parts[items]
#         print(merged_num)
#         merged_parts.append(merged_num)
#         items += 1
#
#     print(sorted_parts)
#     print (sum(merged_parts))
#
#
# minimumTime(4, [8, 4 , 6 ,12])

# def minnode(n, keyval, mstset):
#     mini = 999999999999
#     mini_index = None
#
#     # Loop through all the values of
#     # the nodes which are not yet
#     # included in MST and find the
#     # minimum valued one.
#     for i in range(n):
#         if (mstset[i] == False and
#             keyval[i] < mini): mini = keyval[i]
#         mini_index = i
#     return mini_index
# # Function to find out the MST and # the cost of the MST.
# def findcost(n, city): # Array to store the parent # node of a particular node.
#     parent = [None] * n # Array to store key value # of each node.
#     keyval = [None] * n # Boolean Array to hold bool # values whether a node is # included in MST or not.
#     mstset = [None] * n # Set all the key values to infinite and # none of the nodes is included in MST.
#     for i in range(n):
#         keyval[i] = 9999999999999
#         mstset[i] = False
#         # Start to find the MST from node 0. # Parent of node 0 is none so set -1. # key value or minimum cost to reach # 0th node from 0th node is 0.
#         parent[0] = -1 keyval[0] = 0 # Find the rest n-1 nodes of MST.
#         for i in range(n - 1): # First find out the minimum node # among the nodes which are not yet # included in MST.
#             u = minnode(n, keyval, mstset) # Now the uth node is included in MST.
#             mstset[u] = True # Update the values of neighbor # nodes of u which are not yet
#             # included in MST.
#             for v in range(n):
#                 if (city[u][v] and mstset[v] == False and city[u][v] < keyval[v]):
#                     keyval[v] = city[u][v]
#                     parent[v] = u # Find out the cost by adding # the edge values of MST.
#                     cost = 0
#                     for i in range(1, n):
#                         cost += city[parent[i]][i] print(cost) # Driver Code
#     if __name__ == '__main__': # Input 1
#         n1 = 5
#         city1 = [[0, 1, 2, 3, 4], [1, 0, 5, 0, 7], [2, 5, 0, 6, 0], [3, 0, 6, 0, 0], [4, 7, 0, 0, 0]]
#         findcost(n1, city1) # Input 2 n2 = 6 city2 = [[0, 1, 1, 100, 0, 0], [1, 0, 1, 0, 0, 0], [1, 1, 0, 0, 0, 0], [100, 0, 0, 0, 2, 2], [0, 0, 0, 2, 0, 2], [0, 0, 0, 2, 2, 0]] findcost(n2, city2) # This code is contributed by PranchalK [tabbyending]