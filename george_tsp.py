#!/usr/bin/python

# Copyright 2013, Gurobi Optimization, Inc.

# Solve a traveling salesman problem on a randomly generated set of
# points using lazy constraints.   The base MIP model only includes
# 'degree-2' constraints, requiring each node to have exactly
# two incident edges.  Solutions to this model may contain subtours -
# tours that don't visit every city.  The lazy constraint callback
# adds new constraints to cut them off.

import sys
import math
import random
from gurobipy import *


# Callback - use lazy constraints to eliminate sub-tours
# from roswtf.graph import probe_all_services


def subtourelim(model, where):
    if where == GRB.callback.MIPSOL:
        selected = []
        # make a list of edges selected in the solution
        for i in range(n):
            sol = model.cbGetSolution([model._vars[i,j] for j in range(n)])
            selected += [(i,j) for j in range(n) if sol[j] > 0.5]
        # find the shortest cycle in the selected edge list
        tour = subtour(selected)
        if len(tour) < n:
            # add a subtour elimination constraint
            expr = 0
            for i in range(len(tour)):
                for j in range(i+1, len(tour)):
                    expr += model._vars[tour[i], tour[j]]
            model.cbLazy(expr <= len(tour)-1)


# Euclidean distance between two points

def distance(points, i, j):
    dx = points[i][0] - points[j][0]
    dy = points[i][1] - points[j][1]
    return math.sqrt(dx*dx + dy*dy)


# Given a list of edges, finds the shortest subtour

def subtour(edges):
    visited = [False]*n
    cycles = []
    lengths = []
    selected = [[] for i in range(n)]
    for x,y in edges:
        selected[x].append(y)
    while True:
        current = visited.index(False)
        thiscycle = [current]
        while True:
            visited[current] = True
            neighbors = [x for x in selected[current] if not visited[x]]
            if len(neighbors) == 0:
                break
            current = neighbors[0]
            thiscycle.append(current)
        cycles.append(thiscycle)
        lengths.append(len(thiscycle))
        if sum(lengths) == n:
            break
    return cycles[lengths.index(min(lengths))]


# # Parse argument
#
# if len(sys.argv) < 2:
#     print('Usage: tsp.py npoints')
#     exit(1)
# n = int(sys.argv[1])
#
# # Create n random points
#
n = 50

# probs = [0.05,0.06,0.07,0.08,0.09,0.1,0.2,0.21,0.22,0.222,0.061]
# n = len(probs)
random.seed(2)
probs = []
for i in range(n):
     # probs.append(round((i/n),2))
    probs.append(round(random.random(),4))
probs[0] = 1000
origin = []
origin.append(1)
probs[:0] = origin

m = Model()


# Create variables

vars = {}
for i in range(n+1):
    for j in range(n+1):
        if j == 0:
            value = 0
        else:
            value = probs[j]/probs[i]
        vars[i,j] = m.addVar(obj=value, vtype=GRB.BINARY,
                             name='e'+str(i)+'_'+str(j))
m.update()

uVars = {}
for i in range(n+1):
    uVars[i] = m.addVar(vtype=GRB.INTEGER,name='u'+str(i))
m.update()


# Noone exits the origin
m.addConstr(quicksum(vars[0,j] for j in range(n+1)) == 0)
m.update()

#For all the others someone exits
for i in range(1,n+1):
    m.addConstr(quicksum(vars[i,j] for j in range(n+1)) == 1)
m.update()

#Noone enters the begining position
m.addConstr(quicksum(vars[i,1] for i in range(n+1)) == 0)
m.update()

#For all the others someone enters
for j in range(n+1):
    if j != 1:
        m.addConstr(quicksum(vars[i,j] for i in range(n+1)) == 1)
m.update()

for i in range(1,n):
    for j in range(1,n):
        if (i != j):
            m.addConstr(uVars[i]-uVars[j]+(n-1)*vars[i,j] <= n-2)
m.update()

m.write("tsp.lp")

# Optimize model

m._vars = vars
m._uVars = uVars


# m.params.LazyConstraints = 1
# m.optimize(subtourelim)
m.optimize()
solution = m.getAttr('X', vars)


selected = [(i,j) for i in range(n+1) for j in range(n+1) if solution[i,j] > 0.5]
# assert len(subtour(selected)) == n

print(probs)
print('')
print(len(probs))
print(selected)
# print('Optimal tour: %s' % str(subtour(selected)))
print('Optimal cost: %g' % m.objVal)
print('')
