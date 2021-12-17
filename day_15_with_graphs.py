# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 12:56:31 2021

@author: WESTMR
"""

import numpy as np
import networkx as nx

#%%

def make_cave_array(cave_str):
    return np.array([list(row) for row in cave_str]).astype(int)

with open('inputs/input_15.txt') as the_data:
    live_cave = the_data.read().strip('\n').split('\n')

live_cave = make_cave_array(live_cave)

test_cave = '''
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
'''.strip('\n').split('\n')

def make_cave_array(cave_str):
    return np.array([list(row) for row in cave_str]).astype(int)

test_cave = make_cave_array(test_cave)

#%% Utility Functions

def in_bounds(tup,bounds):
    return all( a>=0 for a in tup) and all(tup[i]<bounds[i] for i in range(len(tup)))

def add(t1,t2):
    return tuple(t1[i] + t2[i] for i in range(len(t1)))

#%% Functions to build the weighted directed graphs

def edges_from(tup,weights):
    to_return = []
    for d in [(1,0),(0,1),(-1,0),(0,-1)]:
        new = add(tup,d)
        if in_bounds(new,weights.shape):
            to_return.append((tup,new,weights[new]))
    return to_return
    
def make_graph(cave_array):
    G = nx.DiGraph()
    G.add_nodes_from([(a,b) for a in range(cave_array.shape[0]) for b in range(cave_array.shape[1])])
    for n in G.nodes():
        G.add_weighted_edges_from(edges_from(n,cave_array))
    
    return G

#%% Part 1: Find the shortest path from the top left to the bottom right.
    
G = make_graph(live_cave)

length,path = nx.single_source_dijkstra(G,source=(0,0), target = add(live_cave.shape,(-1,-1)),weight='weight')

#%% Part 2: Actually that wasn't the whole cave, it was just a portion of the whole cave.

# Here we multiply the size of the cave by 5 and add one for each step the repeat is away from the start

def extend_array(cave,n=5):
    w, h = cave.shape
    new_cave = np.zeros((w*5,h*5))
    for i in range(5):
        for j in range(5):
            new_cave[i*w:(i+1)*w,j*w:(j+1)*w] = (cave+i+j)
    while (new_cave>9).any():
        new_cave = np.where(new_cave>9,new_cave-9,new_cave)
    return new_cave

full_cave = extend_array(live_cave)

#%% Part 2 solution

G2 = make_graph(full_cave)

length,path = nx.single_source_dijkstra(G2,source=(0,0),target=add(full_cave.shape,(-1,-1)),weight='weight')


