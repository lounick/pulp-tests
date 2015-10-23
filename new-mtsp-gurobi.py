__author__ = 'nick'

import sys
import math
import random
from gurobipy import *

n = 7
L = 5
K = 0
salesmen = 3

def distance(points, i, j):
    dx = points[i][0] - points[j][0]
    dy = points[i][1] - points[j][1]
    return math.sqrt(dx*dx + dy*dy)

random.seed(1)
points = []
points.append((0, 0))
points.append((1, 1))
points.append((1, 2))
points.append((1, 3))
points.append((-1, 1))
points.append((-1, 2))
points.append((-1, 3))
# print(n)
# for i in range(n-1):
#     points.append((random.randint(0, 100), random.randint(0, 100)))

m = Model()

# Create variables

vars = {}

for i in range(n):
    for j in range(n):
        vars[i, j] = m.addVar(obj=distance(points, i, j), vtype=GRB.BINARY, name='e_'+str(i)+'_'+str(j))
m.update()

uVars = {}
for i in range(n):
    uVars[i] = m.addVar(vtype=GRB.INTEGER, name='u_'+str(i))#lb=K, ub=L, vtype=GRB.INTEGER, name='u_'+str(i))
    #vars[i, i].ub = 0
m.update()

m.addConstr(quicksum(vars[0, i] for i in range(1, n)) == salesmen)
m.update()

m.addConstr(quicksum(vars[i, 0] for i in range(1, n)) == salesmen)
m.update()

for j in range(1, n):
    m.addConstr(quicksum(vars[i, j] for i in range(n)) == 1)
m.update()

for i in range(1, n):
    m.addConstr(quicksum(vars[i, j] for j in range(n)) == 1)
m.update()

for i in range(1, n):
    m.addConstr(uVars[i] + (L - 2)*vars[0, i] - vars[i, 0] <= (L - 1))
m.update()

for i in range(1, n):
    m.addConstr(uVars[i] + vars[0, i] + (2 - K)*vars[i, 0] >= 2)
m.update()

for i in range(1, n):
    m.addConstr(vars[0, i] + vars[i, 0] <= 1)
m.update()

for i in range(1, n):
    for j in range(1, n):
        if i != j:
            m.addConstr(uVars[i] - uVars[j] + L*vars[i, j] + (L - 2)*vars[j, i] <= (L - 1))
m.update()

m.write("mtsp.lp")

m.update()

totVars = dict(list(vars.items())+list(uVars.items()))
m._vars = vars
m._uvars = uVars

m.optimize()

solution = m.getAttr('x', vars)
selected = [(i,j) for i in range(n) for j in range(n) if solution[i,j] > 0.5]

uValues = m.getAttr('x', uVars)
print("U values: ", uValues)

print('')
print('Optimal tour: %s' % str(selected))
print('Optimal cost: %g' % m.objVal)
print('')