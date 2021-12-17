# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 13:56:40 2021

@author: WESTMR
"""

conv_dict = {str(a):bin(a)[2:] for a in range(10)}
for l in ['A','B','C','D','E','F']:
    conv_dict[l] = bin(int(l,base=16))[2:]
for l in conv_dict:
    while len(conv_dict[l])<4:
        conv_dict[l] = '0' + conv_dict[l]
print(conv_dict)

def conv_hex_to_bin(hex_num):
    new_num = ''
    for d in hex_num:
        new_num += conv_dict[d]
    return new_num

#%%

def read_literal(long_string):
    string_num = ''
    while long_string[0] != '0':
        string_num += long_string[1:5]
        long_string = long_string[5:]
    string_num += long_string[1:5]
    long_string = long_string[5:]
    dec_num = int(string_num,base=2)
    return dec_num, long_string

def read_packet(long_string,versions):
    version = int(long_string[:3],base=2)
    versions.append(version)
    packet_type = int(long_string[3:6],base=2)
    long_string = long_string[6:]
    if packet_type == 4:
        val, long_string = read_literal(long_string)
        packets = [version,packet_type,val]
    else:
        ID = long_string[0]
        long_string = long_string[1:]
        subs_as_lists = []
        if ID == '0':
            total_length = long_string[:15]
            long_string = long_string[15:]
            num_bits = int(total_length,base=2)
            subpackets = long_string[:num_bits]
            long_string = long_string[num_bits:]
            while '1' in subpackets:
                subpackets, this_sub, versions = read_packet(subpackets,versions)
                subs_as_lists.append(this_sub)
        elif ID == '1':
            total_num = long_string[:11]
            long_string = long_string[11:]
            num_subs = int(total_num,base=2)
            while len(subs_as_lists) != num_subs:
                long_string, this_sub, versions = read_packet(long_string,versions)
                subs_as_lists.append(this_sub)
        packets = [version,packet_type,ID,subs_as_lists]
    #long_string = long_string.lstrip('0')      
    return long_string,packets, versions

#%%

versions_1 = []
test_hex_1 = 'D2FE28'
test_bin_1 = bin(int(test_hex_1,base = 16))[2:]
read_packet(test_bin_1,versions_1)

#%%

versions_2 = []
test_hex_2 = '38006F45291200'
test_bin_2 = conv_hex_to_bin(test_hex_2)
read_packet(test_bin_2,versions_2)

#%%

versions_3 = []
test_hex_3 = 'EE00D40C823060'
test_bin_3 = conv_hex_to_bin(test_hex_3)
read_packet(test_bin_3,versions_3)

#%%

versions_4 = []
test_hex_4 = '8A004A801A8002F478'
test_bin_4 = conv_hex_to_bin(test_hex_4)
read_packet(test_bin_4,versions_4)

#%%

def get_sum_versions(hex_num):
    the_versions = []
    bin_num = conv_hex_to_bin(hex_num)
    read_packet(bin_num,the_versions)
    return sum(the_versions)

get_sum_versions('8A004A801A8002F478')
get_sum_versions('620080001611562C8802118E34')
get_sum_versions('C0015000016115A2E0802F182340')
get_sum_versions('A0016C880162017C3686B18A3D4780')


#%%

with open('inputs/input_16.txt') as the_data:
    my_hex = the_data.read().strip('\n').strip()
get_sum_versions(my_hex)


#%% Part 2 - Similar but more
import numpy as np
def read_packet_part2(long_string):
    version = int(long_string[:3],base=2)
    packet_type = int(long_string[3:6],base=2)
    long_string = long_string[6:]
    if packet_type == 4:
        val, long_string = read_literal(long_string)
    else:
        ID = long_string[0]
        long_string = long_string[1:]
        subs_vals = []
        lens = {'0':15,'1':11}
        first_val = int(long_string[:lens[ID]],base=2)
        long_string = long_string[lens[ID]:]
        if ID == '0':
            subpackets = long_string[:first_val]
            long_string = long_string[first_val:]
            while '1' in subpackets:
                subpackets, this_sub = read_packet_part2(subpackets)
                subs_vals.append(this_sub)
        elif ID == '1':
            while len(subs_vals) != first_val:
                long_string, this_sub = read_packet_part2(long_string)
                subs_vals.append(this_sub)
    packet_types = [np.sum,np.prod,np.min,np.max,'literal',int.__gt__,int.__lt__,int.__eq__]
    if packet_type < 2:
        val = int(packet_types[packet_type](subs_vals,dtype=np.int64))
    elif packet_type < 4:
        val = int(packet_types[packet_type](subs_vals))
    elif packet_type > 4:
        assert len(subs_vals)==2
        comp = packet_types[packet_type]
        val = int(comp(int(subs_vals[0]),int(subs_vals[1])))
    return long_string, val

#%%
    
assert read_packet_part2(conv_hex_to_bin('C200B40A82'))[1] == 3
assert read_packet_part2(conv_hex_to_bin('04005AC33890'))[1] == 54
assert read_packet_part2(conv_hex_to_bin('880086C3E88112'))[1] == 7
assert read_packet_part2(conv_hex_to_bin('D8005AC2A8F0'))[1] == 1
assert read_packet_part2(conv_hex_to_bin('F600BC2D8F'))[1] == 0
assert read_packet_part2(conv_hex_to_bin('9C005AC2F8F0'))[1] == 0
assert read_packet_part2(conv_hex_to_bin('9C0141080250320F1802104A08'))[1] == 1

#%%
read_packet_part2(conv_hex_to_bin(my_hex))