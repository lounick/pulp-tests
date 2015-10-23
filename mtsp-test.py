__author__ = 'nick'

from pulp import *
import numpy as np

def findEucledianDistance (point1, point2):
    return np.linalg.norm(point1 - point2)

def findDistances(points):
    distMat = np.zeros((points.shape[0],points.shape[0]))
    for i in range(0,points.shape[0]):
        for j in range(i+1, points.shape[0]):
            distMat[i, j] = findEucledianDistance(points[i], points[j])
            distMat[j, i] = distMat[i, j]
    return distMat

a = np.array([0,0])
b = np.array([1,3])
c = np.array([3,3])
d = np.array([-1,3])
e = np.array([-3,3])

# cities = ['A', 'B', 'C', 'D', 'E']
#
# points = np.append([a], [b], axis=0)
# points = np.append(points, [c], axis=0)
# points = np.append(points, [d], axis=0)
# points = np.append(points, [e], axis=0)
#
# # print(points)
#
# # print(findDistances(points))
#
# distances = findDistances(points)
#
# print(distances)

# distnaces =[
#          #1  2  3  4  5
#          [0, 4, 5, 2, 1], #1
#          [3, 0, 3, 2, 3], #2
#          [3, 1, 0, 2, 3], #3
#          [3, 1, 3, 0, 3], #4
#          [3, 1, 3, 2, 0], #5
#         ]

cities = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
distances = [
         #1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
         [0, 509, 501, 312, 1019, 736, 656, 60, 1039, 726, 2314, 479, 448, 479, 619, 150], #1
         [509, 0, 126, 474, 1526, 1226, 1133, 532, 1449, 1122, 2789, 958, 941, 978, 1127, 542], #2
         [501, 126, 0, 541, 1516, 1184, 1084, 536, 1371, 1045, 2728, 913, 904, 946, 1115, 499], #3
         [312, 474, 541, 0, 1157, 980, 919, 271, 1333, 1029, 2553, 751, 704, 720, 783, 455], #4
         [1019, 1526, 1516, 1157, 0, 478, 583, 996, 858, 855, 1504, 677, 651, 600, 401, 1033], #5
         [736, 1226, 1184, 980, 478, 0, 115, 740, 470, 379, 1581, 271, 289, 261, 308, 687], #6
         [656, 1133, 1084, 919, 583, 115, 0, 667, 455, 288, 1661, 177, 216, 207, 343, 592], #7
         [60, 532, 536, 271, 996, 740, 667, 0, 1066, 759, 2320, 493, 454, 479, 598, 206], #8
         [1039, 1449, 1371, 1333, 858, 470, 455, 1066, 0, 328, 1387, 591, 650, 656, 776, 933], #9
         [726, 1122, 1045, 1029, 855, 379, 288, 759, 328, 0, 1697, 333, 400, 427, 622, 610], #10
         [2314, 2789, 2728, 2553, 1504, 1581, 1661, 2320, 1387, 1697, 0, 1838, 1868, 1841, 1789, 2248], #11
         [479, 958, 913, 751, 677, 271, 177, 493, 591, 333, 1838, 0, 68, 105, 336, 417], #12
         [448, 941, 904, 704, 651, 289, 216, 454, 650, 400, 1868, 68, 0, 52, 287, 406], #13
         [479, 978, 946, 720, 600, 261, 207, 479, 656, 427, 1841, 105, 52, 0, 237, 449], #14
         [619, 1127, 1115, 783, 401, 308, 343, 598, 776, 622, 1789, 336, 287, 237, 0, 636], #15
         [150, 542, 499, 455, 1033, 687, 592, 206, 933, 610, 2248, 417, 406, 449, 636, 0], #16
        ]
costs = pulp.makeDict([cities, cities], distances,0)

# print(costs)

routes = []
for i in cities:
    for j in cities:
        if(i != j):
            routes.append((i,j))


m = 2 #Number of salesmen
L = 3 #Max number of cities a salesman can visit
K = 2 #Minimum number of cities a salesman can visit

prob = pulp.LpProblem("Multiple Travelling Salesmen Problem", pulp.LpMinimize)

x = pulp.LpVariable.dicts("route", (cities, cities), lowBound=0, upBound=1, cat=pulp.LpInteger)

u = pulp.LpVariable.dicts("u", cities, cat=pulp.LpInteger)#, lowBound=0, cat=pulp.LpInteger) #TODO: Do we need the lowBound???

#Objective function
prob += sum([x[w][b]*costs[w][b] for (w, b) in routes]), "Sum_of_Tour_Costs"

#Constraints
tmp = []
for i in cities[1:]:
    tmp.append(x[cities[0]][i])
prob += sum(tmp) == m, "Number of routes from start"

tmp = []
for i in cities[1:]:
    tmp.append(x[i][cities[0]])
prob += sum(tmp) == m, "Number of routes to start"

for i in cities:
    tmp = []
    for j in cities:
        if(i != j):
            tmp.append(x[i][j])
    prob += sum(tmp) == 1, "route_out_%s"%i

for i in cities:
    tmp = []
    for j in cities:
        if(i != j):
            tmp.append(x[j][i])
    prob += sum(tmp) == 1, "route_in_%s"%i

for i in cities[1:]:
    prob += u[i] + (L-2)*x[cities[0]][i] - x[i][cities[0]] <= L-1

for i in cities[1:]:
    prob += u[i] + x[cities[0]][i] + (2-K)*x[i][cities[0]] >= 2

for i in cities[1:]:
    prob += x[cities[0]][i] + x[i][cities[0]] <=1

for i in cities[1:]:
    for j in cities[1:]:
        if (i != j):
            prob += u[i] - u[j] +L*x[i][j] +(L-2)*x[j][i] <= L-1

prob.writeLP("MTSP.lp")

prob.solve()

print("Status:", pulp.LpStatus[prob.status])

for v in prob.variables():
    print(v.name, "=", v.varValue)

print("Total Cost of Transportation = ", prob.objective.value())
