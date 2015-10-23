__author__ = 'nick'

from pulp import amply

data = amply.Amply("set CITIES := Auckland Wellington Christchurch;")

print(data['CITIES'])

for c in data.CITIES: print(c)

print(data.CITIES[0])

print(len(data.CITIES))

data = amply.Amply("""set BitsNPieces := 0 3.2 -6e4 Hello "Hello, World!";""")

print(data.BitsNPieces)

data = amply.Amply("""set pairs dimen 2;set pairs := (1, 2) (2, 3) (3, 4);""")

print(data.pairs)

data = amply.Amply("""set CITIES{COUNTRIES};set CITIES[Australia] := Adelaide Melbourne Sydney;set CITIES[Italy] := Florence Milan Rome;""")

print(data.CITIES['Australia'])

print(data.CITIES['Italy'])

data = amply.Amply("set SUBURBS{COUNTRIES, CITIES};set SUBURBS[Australia, Melbourne] := Docklands 'South Wharf' Kensington;")

print(data.SUBURBS['Australia', 'Melbourne'])

# data = amply.Amply("set TRIPLES dimen 3; set TRIPLES := (1,1,*) 2 3 4 (*,2*) 6 7 8 9 (*,*,*) (1,1,1)")
data = amply.Amply("""set TRIPLES dimen 3;set TRIPLES := (1, 1, *) 2 3 4 (*, 2, *) 6 7 8 9 (*, *, *) (1, 1, 1);""")

print(data.TRIPLES)

data = amply.Amply("""set ROUTES dimen 2; set ROUTES : A B C D := E + - - + F + + - -;""")

print(data.ROUTES)

data = amply.Amply("""set ROUTES dimen 2; set ROUTES (tr) : E F := A + + B - + C - - D + - ;""")

print(data.ROUTES)

data = amply.Amply("""set QUADS dimen 2; set QUADS := (1, 1, *, *) : 2 3 4 := 2 + - + 3 - + + (1, 2, *, *) : 2 3 4 := 2 - + - 3 + - -;""")

print(data.QUADS)

data = amply.Amply("""param T := 30; param n := 5;""")

print(data.T)

print(data.n)

data = amply.Amply("""param COSTS{PRODUCTS}; param COSTS := FISH 8.5 CARROTS 2.4 POTATOES 1.6;""")

print(data.COSTS)

print(data.COSTS['FISH'])

data = amply.Amply("""param COSTS{P}; param COSTS default 2 := F 2 E 1 D . ;""")

print(data.COSTS['D'])

data = amply.Amply(""" param COSTS{P} default 42; param COSTS := F 2 E 1 ;""")

print(data.COSTS['DOES NOT EXIST'])

data = amply.Amply("""
param COSTS{CITIES, PRODUCTS};
param COSTS :=
Auckland FISH 5
Auckland CHIPS 3
Wellington FISH 4
Wellington CHIPS 1
;
""")

print(data.COSTS)

print(data.COSTS['Wellington']['CHIPS'])

print(data.COSTS['Wellington', 'CHIPS'])

data = amply.Amply("""
param COSTS{CITIES, PRODUCTS};
param COSTS :=
[Auckland, * ]
 FISH 5
 CHIPS 3
[Wellington, * ]
 FISH 4
 CHIPS 1
;
""")

print(data.COSTS)

data = amply.Amply("""
param COSTS{CITIES, PRODUCTS};
param COSTS: FISH CHIPS :=
Auckland    5    3
Wellington  4    1
;
""")

print(data.COSTS)

data = amply.Amply("""
param COSTS{CITIES, PRODUCTS};
param COSTS (tr): Auckland Wellington :=
FISH   5        4
CHIPS  3        1
;
""")

print(data.COSTS)

data = amply.Amply("""
param COSTS{CITIES, PRODUCTS, SIZE};
param COSTS :=
[Auckland, *, *] :   SMALL LARGE :=
                FISH  5     9
                CHIPS 3     5
[Wellington, *, *] : SMALL LARGE :=
                FISH  4     7
                CHIPS 1     2
;
""")

print(data.COSTS)

data = amply.Amply("set CITIES := Auckland Hamilton Wellington;")

# attribute lookup
assert data.CITIES == ['Auckland', 'Hamilton', 'Wellington']

# item lookup
assert data['CITIES'] == data.CITIES
