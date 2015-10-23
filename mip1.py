__author__ = 'nick'

#!/usr/bin/python

# Copyright 2013, Gurobi Optimization, Inc.

# This example formulates and solves the following simple MIP model:
# maximize
#        x +   y + 2 z
#  subject to
#        x + 2 y + 3 z <= 4
#        x +   y       >= 1
#  x, y, z binary

import sys
import math
import random
import time
from gurobipy import *


# Callback - use lazy constraints to eliminate sub-tours

def subtourelim(model, where):
    try:
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
                if expr:
                    model.cbLazy(expr <= len(tour)-1)
    except GurobiError as inst:
        print("ERROR!!!!!!")
        print(inst.message)

def subtourelim1(model, where):
    try:
        if where == GRB.callback.MIPSOL:
            selected = []
            # make a list of edges selected in the solution
            for i in range(n):
                sol = model.cbGetSolution([model._vars[i,j] for j in range(n)])
                selected += [(i,j) for j in range(n) if sol[j] > 0.5]
                # print(selected)
            # find the shortest cycle in the selected edge list
            for item in selected:
                # Other constraint
                # if (item[0] != 0 and item[1] != 0):
                #     model.cbLazy(model._uVars[item[0]] - model._uVars[item[1]] + (n - salesmen) * model._vars[item[0], item[1]] <= n - salesmen - 1)
                # Bektas constraints
                if item[0] == 0:
                    model.cbLazy(model._uVars[item[1]] + (L - 2) * model._vars[0,item[1]] - model._vars[item[1],0] <= L - 1)
                    model.cbLazy(model._uVars[item[1]] + model._vars[0,item[1]] + (2 - K) * model._vars[item[1],0] >= 2)
                    model.cbLazy(model._vars[0,item[1]] + model._vars[item[1],0] <= 1)
                if item[1] == 0:
                    model.cbLazy(model._uVars[item[0]] + (L - 2) * model._vars[0,item[0]] - model._vars[item[0],0] <= L - 1)
                    model.cbLazy(model._uVars[item[0]] + model._vars[0,item[0]] + (2 - K) * model._vars[item[0],0] >= 2)
                    model.cbLazy(model._vars[0,item[0]] + model._vars[item[0],0] <= 1)
                if (item[0] != 0 and item[1] != 0):
                    model.cbLazy(model._uVars[item[0]] - model._uVars[item[1]] + L * model._vars[item[0],item[1]] + (L - 2) * model._vars[item[1],item[0]] <= L - 1)

    except GurobiError as inst:
        print("ERROR!!!!!!")
        print(inst.message)


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
try:

    L = 20
    K = 4
    salesmen = 3

    if len(sys.argv) < 2:
        print('Usage: tsp.py npoints')
        exit(1)
    n = int(sys.argv[1])

    # Create n random points

    random.seed(time.time())
    points = []
    for i in range(n):
        points.append((random.randint(0, 100), random.randint(0, 100)))
    # points = []
    # points.append((0,0))
    # points.append((1,3))
    # points.append((3,3))
    # points.append((-1,3))
    # points.append((-3,3))
    # Create a new model

    # points = []
    # f = open('pr76.tsp', 'r')
    #
    # cities = []
    # begin = False
    # for line in f:
    #     line = line.rstrip('\n')
    #     parsedline = line.split()
    #     # print(parsedline)
    #     if line == "EOF":
    #         begin = False
    #     if begin:
    #         points.append((int(parsedline[1]),int(parsedline[2])))
    #     if line == "NODE_COORD_SECTION":
    #         begin = True
    #     if parsedline[0] == "DIMENSION":
    #         n = int(parsedline[2])

    m = Model("mTSP")

    vars = {}
    for i in range(n):
        for j in range(n):
            vars[i, j] = m.addVar(vtype=GRB.BINARY, name='e_' + str(i) + '_' + str(j))
            # vars[i, i].ub = 0

    uVars = {}
    for i in range(n):
        uVars[i] = m.addVar(vtype=GRB.INTEGER, name='u' + str(i))

    m.update()

    # Set objective
    m.setObjective(quicksum(distance(points, i, j) * vars[i, j] for i in range(n) for j in range(n) if i != j),
                   GRB.MINIMIZE)
    m.update()

    m.addConstr(quicksum(vars[0, i] for i in range(1, n)) == salesmen)
    m.update()

    m.addConstr(quicksum(vars[i, 0] for i in range(1, n)) == salesmen)
    m.update()

    for j in range(1, n):
        m.addConstr(quicksum(vars[i, j] for i in range(n)) == 1)
    m.update()

    for i in range(n):
        vars[i, i].ub = 0
    m.update()

    for i in range(1, n):
        m.addConstr(quicksum(vars[i, j] for j in range(n)) == 1)
    m.update()

    # Other Constraint
    # for i in range(1, n):
    #     for j in range(1, n):
    #         if i != j:
    #             m.addConstr(uVars[i] - uVars[j] + (n - salesmen) * vars[i, j] <= n - salesmen - 1)
    # m.update()

    # Bektas constraints
    for i in range(1,n):
        m.addConstr(uVars[i] + (L - 2) * vars[0, i] - vars[i, 0] <= L - 1)
    m.update()

    for i in range(1,n):
        m.addConstr(uVars[i] + vars[0, i] + (2 - K) * vars[i, 0] >= 2)
    m.update()

    for i in range(1,n):
        m.addConstr(vars[0, i] + vars[i,0] <= 1)
    m.update()

    for i in range(1,n):
        for j in range(1,n):
            if i != j:
                m.addConstr(uVars[i] - uVars[j] + L * vars[i,j] + (L - 2) * vars[j,i] <= L -1)
    m.update()

    m.write("newMTSP.lp")

    m._vars = vars
    m._uVars = uVars

    print(m._vars)
    print(m._uVars)

    # m.computeIIS()
    # m.write("inewMTSP.ilp")
    # m.params.LazyConstraints = 1
    # m.optimize(subtourelim1)
    m.optimize()

    for v in m.getVars():
        if v.x == 1:
            print('%s %g' % (v.varName, v.x))

except GurobiError:
    print('Error reported')