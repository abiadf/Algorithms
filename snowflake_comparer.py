# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 11:29:23 2022
@author: Fouad
"""

import numpy as np
from collections import Counter

N_FLAKE = int(1e1) #number of snowflakes to compare

L_FLAKE = 6 #how many legs in a snowflake
W_FLAKE = 1 #how may snowflakes at a time (= per row)

MIN_LENGTH = 1 #minimum leg length
MAX_LENGTH = 6 #maximum leg length

S_SNOWFLAKE = [W_FLAKE, L_FLAKE] #size of snowflake array

#Generating N snowflakes of random lengths
snowflakes = np.empty([N_FLAKE, L_FLAKE]) #empty array of 6 columns
for i in range(N_FLAKE):
    snowflakes[i,:] = np.random.randint(MIN_LENGTH, MAX_LENGTH+1, S_SNOWFLAKE) #snowflake lengths

#Getting frequency of snowflake perimeters
perimeter = np.sum(snowflakes, axis=1) #sum legs of each snowflake
perimeter_freq = Counter(perimeter).most_common() #(most frequent, frequency) tuple
# print(perimeter_freq)


#Make array to store the indices of different perimeters
different_perimeters = len(perimeter_freq) #how many unique perimeters are there
highest_perimeter = perimeter_freq[0][1] #maximum perimeter is found on index 0 of the perimeter list from Couter().most_common()
index_perimeter = -np.ones([different_perimeters, highest_perimeter] ) #table showing different indices of different perimeters. set to -1 to know when the array is over

# Loop through the frequency of appearance of the sum
for i in range(len(perimeter_freq)):
    # print(perimeter_freq[i][1])
    
    index_locator = np.where(perimeter == perimeter_freq[i][0]) #gives indices of snowflakes who share the same perimeter of this iteration
    # print( index_locator[0] )

    for j in index_locator:
        index_perimeter[i, 0:len(j)] = j

print(index_perimeter)


same_perimeters = np.zeros( [N_FLAKE, L_FLAKE] ) #table showing different indices of different perimeters. set to -1 to know when the array is over

#Cluster same-perimeter flakes together
counter = 0
for idx,val in enumerate(index_perimeter):
    for j in val:
        if j > -1:
            same_perimeters[counter, :] = snowflakes[int(j), :]
            counter += 1

print(same_perimeters)

#Compare snowflakes of same perimeter
counter = 0
for idx, val in enumerate(index_perimeter):
    for j in val:
        if j > -1:
            print(j)
            
            counter += 1
            # np.array_equal(snowflakes[index_perimeter][0], snowflakes[index_perimeter][j])
#     # # #         # compare(i,0) == index_perimeter[i][j]
#     #         # print(snowflakes[idx] )
#             print(j)

