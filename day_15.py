# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 17:48:42 2021

@author: WESTMR
"""
#%%

import numpy as np

#%%

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

#%%

def add(t1,t2):
    return tuple(t1[i] + t2[i] for i in range(len(t1)))

def in_bounds(tup,bounds):
    return all( a>=0 for a in tup) and all(tup[i]<bounds[i] for i in range(len(tup)))

def get_first_path(cave_scores):
    v1 = min(sum(cave_scores[0,:i+1]) + sum(cave_scores[:,i]) + sum(cave_scores[i:,-1]) for i in range(cave_scores.shape[1]))
    v2 = min(sum(cave_scores.transpose()[0,:i+1]) + sum(cave_scores.transpose()[:,i]) + sum(cave_scores.transpose()[i:,-1]) for i in range(cave_scores.shape[0]))
    return min(v1,v2)
    

start_paths = [[(0,0),(1,0)],[(0,0),(0,1)]]

#%%
    
min_path_score = get_first_path(test_cave)

def is_ok_to_add(path,path_score,new,cave_scores,min_score_found):
    if new in path:
        return False
    elif not in_bounds(new,cave_scores.shape):
        return False
    elif cave_scores[new] + path_score > min_score_found:
        return False
    elif any(add(new,d) in path[:-1] for d in [(1,0),(-1,0),(0,1),(0,-1)]):
        return False
    else:
        return True
    
    

def iterate_path(path,cave_scores,min_path_score):
    last = path[-1]
    path_score = sum([cave_scores[s] for s in path[1:]])
    if last == add(cave_scores.shape,(-1,-1)) and path_score <= min_path_score:
        return [path], path_score
    elif path_score > min_path_score:
        return [],min_path_score
    else:
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        new_paths = [path + [add(last,d)] for d in dirs if\
                             is_ok_to_add(path,path_score,add(last,d),\
                                          cave_scores,min_path_score)]
        return new_paths,min_path_score

#%%
        
min_score = get_first_path(test_cave)
poss_paths = start_paths.copy()
i = 0
while any(p[-1] != add(test_cave.shape,(-1,-1)) for p in poss_paths):
    new_paths = []
    for p in poss_paths:
        paths, new_min_score = iterate_path(p,test_cave,min_score)
        new_paths += paths
        min_score = min(new_min_score, min_score)
    poss_paths = new_paths.copy()
    if i%10==0:
        print(i)
    i +=1
print(poss_paths)
print(min_score)
    
#%%
    
with open('inputs/input_15.txt') as the_data:
    live_cave = the_data.read().strip('\n').split('\n')

live_cave = make_cave_array(live_cave)


min_score = get_first_path(live_cave)
poss_paths = start_paths.copy()
i = 0
while any(p[-1] != add(live_cave.shape,(-1,-1)) for p in poss_paths):
    new_paths = []
    for p in poss_paths:
        paths, new_min_score = iterate_path(p,live_cave,min_score)
        new_paths += paths
        min_score = min(new_min_score, min_score)
    poss_paths = new_paths.copy()
    if i%10==0:
        print(i)
    i +=1
print(poss_paths)
print(min_score)