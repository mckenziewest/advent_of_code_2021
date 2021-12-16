# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 16:38:28 2021

@author: WESTMR
"""

#%%
with open('inputs/input_14.txt') as the_data:
    starting = the_data.readline().strip('\n')
    replaces = the_data.read().strip('\n').split('\n')


#%%
    
insertion_dict = {a[0:2]:a[-1] for a in replaces}

pair_dict = {k:0 for k in insertion_dict}
for i in range(len(starting)-1):
    pair_dict[starting[i:i+2]] += 1

#%%

def do_next(string,ins_dict):
    new_string = string[0]
    for i in range(len(string)-1):
        new_string += ins_dict[string[i:i+2]] + string[i+1]
    return new_string

#%%

def insert_n_times(n,string,ins_dict):
    for i in range(n):
        string = do_next(string,ins_dict)
    return string

#%%

from collections import Counter
def most_minus_least(n,string,ins_dict):
    new_string = insert_n_times(n,string,ins_dict)
    num_chars = Counter(new_string).values()
    return max(num_chars)-min(num_chars)

#%%
print("Part 1 Solution - Keeping the String Around")
print(most_minus_least(10,starting,insertion_dict))

# This takes way too much time for 40 rounds because that's a massive string.
# We change our tactic to keep track of the number of each of the pairs that 
# exist in the string.

#%%
from collections import defaultdict

def do_round(ins_dict,pair_dict):
    npd = defaultdict(int)
    for k in ins_dict.keys():
        npd[k[0] + ins_dict[k]] += pair_dict[k]
        npd[ins_dict[k] + k[1]] += pair_dict[k]
    return npd

def do_n_rounds(n,ins_dict,pair_dict):
    npd = pair_dict.copy()
    for i in range(n):
        npd = do_round(ins_dict,npd)
    return npd

def most_minus_least_char(pair_dict,increase_by_one=starting[-1]):
    char_vals = defaultdict(int)
    for k in pair_dict.keys():
        char_vals[k[0]] += pair_dict[k]
    char_vals[increase_by_one] += 1
    return max(char_vals.values()) - min (char_vals.values())

print("Part 2 Solution")
print(most_minus_least_char(do_n_rounds(40,insertion_dict,pair_dict)))
    