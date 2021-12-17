# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 16:24:50 2021

@author: WESTMR
"""

minx = 175
maxx = 227
miny = -134
maxy = -79

hits = []

#%%

def x_t(t,xv):
    if t <= xv:
        x = sum(xv-a for a in range(t))
    else:
        x = sum(xv-a for a in range(xv))
    return x

#%%

def y_t(t,yv):
    return t*yv - int(t*(t-1)/2)

#%%
def yv_t(t,y): 
    vel_to_hit = (t-1)/2+y/t
    if int(vel_to_hit) == vel_to_hit:
        return vel_to_hit
    

#%%

min_xvel = 1
while x_t(min_xvel,min_xvel)< minx:
    min_xvel+=1

max_xvel = maxx

min_yvel=miny

max_yvel = 133

#%%


## Solution for part 1
for t in range(min_xvel,600):
    for yhit in range(miny,maxy+1): 
        yvel = yv_t(t,yhit)
        if yvel!= None:
            hits += [(19,int(yvel)),(20,int(yvel))]
            max_point = y_t(yvel,yvel)
print(max_point)

#%%

for xvel in range(0,maxx+1):
    p_times = [t for t in range(min_xvel) if x_t(t,xvel) >= minx and x_t(t,xvel) <= maxx]
    for yhit in range(miny,maxy+1): 
        yvels = [yv_t(t,yhit) for t in p_times if yv_t(t,yhit) != None]
        hits += [(int(xvel),int(yvel)) for yvel in yvels]
print(len(set(hits)))