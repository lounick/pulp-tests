__author__ = 'nick'

import sys
import math
import random
from gurobipy import *

L = 30
K = 10
salesmen = 3
ndepots = 3

# Euclidean distance between two points

def distance(points, i, j):
    dx = points[i][0] - points[j][0]
    dy = points[i][1] - points[j][1]
    return math.sqrt(dx*dx + dy*dy)

# Parse argument

if len(sys.argv) < 2:
    print('Usage: tsp.py npoints')
    exit(1)
n = int(sys.argv[1])

# Create n random points
n = 30
print(n)

random.seed(1)
points = []
for i in range(n):
    points.append((random.randint(0,100),random.randint(0,100)))

m = Model()

# Add depot positions in town lists
depots = []
for i in range(ndepots):
    depots.append((random.randint(0,100),random.randint(0,100)))
points[:0] = depots


# DEBUG
#
# n = 4
# L = 5
# K = 2
# salesmen = 2
# ndepots = 2
# depots = []
# depots.append((1, 1))
# depots.append((-1, -1))
#
# points = []
# points.append((2, 2))
# points.append((2, 3))
# points.append((-2, -2))
# points.append((-2, -3))
#
# points[:0] = depots
#
# print(points)

# DEBUG



# Create variables

vars = {}

for i in range(len(points)):
    for j in range(len(points)):
        if i != j:
            vars[i,j] = m.addVar(obj=distance(points,i,j), vtype=GRB.BINARY,name='e_'+str(i)+'_'+str(j))
m.update()

uVars = {}
for i in range(len(points)):
    uVars[i] = m.addVar(vtype=GRB.INTEGER, name='u_'+str(i))
m.update()

for i in range(ndepots):
    m.addConstr(quicksum(vars[i, j] for j in range(ndepots, len(points))) == 1) #only one salesman allowed per depot have to check how to change it
m.update()

for j in range(ndepots):
    m.addConstr(quicksum(vars[i, j] for i in range(ndepots, len(points))) == 1)
m.update()

for j in range(ndepots, len(points)):
    m.addConstr(quicksum(vars[i, j] for i in range(len(points)) if i != j) == 1)
m.update()

for i in range(ndepots, len(points)):
    m.addConstr(quicksum(vars[i, j] for j in range(len(points)) if i != j) == 1)
m.update()

for i in range(ndepots, len(points)):
    m.addConstr(uVars[i] + (L-2)*quicksum(vars[k,i] for k in range(ndepots)) - quicksum(vars[i,k] for k in range(ndepots)) <= (L-1))
m.update()

for i in range(ndepots, len(points)):
    m.addConstr(uVars[i] + quicksum(vars[k,i] for k in range(ndepots)) + (2 - K)*quicksum(vars[i,k] for k in range(ndepots)) >= 2)
m.update()

for k in range(ndepots):
    for i in range(ndepots, len(points)):
        m.addConstr(vars[k,i] + vars[i,k] <= 1)
m.update()

for i in range(ndepots, len(points)):
    for j in range(ndepots, len(points)):
        if(i != j):
            m.addConstr(uVars[i] - uVars[j] + L*vars[i,j] + (L - 2)*vars[j,i] <= L - 1)
m.update()

# for i in range(len(points)):
#     print(i)
#     for j in range(i+1,len(points)):
#         print("j = " , j)
#         vars[i,j] = m.addVar(obj=distance(points, i, j), vtype=GRB.BINARY,
#                              name='e'+str(i)+'_'+str(j))
#         vars[j,i] = vars[i,j]
# m.update()
#
# uVars = {}
# for i in range(len(points)):
#     uVars[i] = m.addVar(lb=K, ub=L, vtype=GRB.INTEGER, name='u'+str(i))
# m.update()
#
# # for i in range(ndepots):
# #     for j in range(ndepots,n+ndepots):
# #         pass
#
# for i in range(ndepots):
#     m.addConstr(quicksum(vars[i, j] for j in range(ndepots, len(points))) == salesmen)
# m.update()
#
# for i in range(ndepots):
#     m.addConstr(quicksum(vars[j, i] for j in range(ndepots, len(points))) == salesmen)
# m.update
#
#
# for j in range(ndepots, len(points)):
#     m.addConstr(quicksum(vars[i, j] for i in range(len(points)) if i != j) == 1)
# m.update()
#
# for i in range(ndepots, len(points)):
#     m.addConstr(quicksum(vars[i, j] for j in range(len(points)) if i != j) == 1)
# m.update()
#
# for i in range(ndepots, len(points)):
#     m.addConstr(uVars[i] + (L-2)*quicksum(vars[k,i] for k in range(ndepots)) - quicksum(vars[i,k] for k in range(ndepots)) <= (L-1))
# m.update()
#
# for i in range(ndepots, len(points)):
#     m.addConstr(uVars[i] + quicksum(vars[k,i] for k in range(ndepots)) + (2 - K)*quicksum(vars[i,k] for k in range(ndepots)) >= 2)
# m.update()
#
# for k in range(ndepots):
#     for i in range(ndepots, len(points)):
#         m.addConstr(vars[k,i] + vars[i,k] <= 1)
# m.update()
#
# for i in range(ndepots, len(points)):
#     for j in range(ndepots, len(points)):
#         if(i != j):
#             m.addConstr(uVars[i] - uVars[j] + L*vars[i,j] + (L - 2)*vars[j,i] <= L - 1)
# m.update()

m.write("mmtsp.lp")

# Optimize model
totVars = dict(list(vars.items())+list(uVars.items()))
m._vars = vars
m._uvars = uVars
# m.params.LazyConstraints = 1
# m.optimize(subtourelim)
m.optimize()

solution = m.getAttr('x', vars)

soluvars = m.getAttr('x', uVars)

print("uVars: ", soluvars)

# for i in range(len(points)):
#     for j in range(len(points)):
#         if i != j:
#             if solution[i, j] > 0.5:
#                 pass
#             print((i, j), ":", solution[i, j])


selected = [(i,j) for i in range(len(points)) for j in range(len(points)) if i != j if solution[i,j] > 0.5]
# assert len(subtour(selected)) == n

print('')
print('Optimal tour: %s' % str(selected))
print('Optimal cost: %g' % m.objVal)
print('')