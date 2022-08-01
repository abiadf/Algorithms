# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 11:29:23 2022
@author: Fouad
"""

import numpy as np
from collections import Counter

# %%
# CONSTANTS
# =========

N_FLAKE = int(1e1) #number of snowflakes to compare

L_FLAKE = 6 #how many legs in a snowflake
W_FLAKE = 1 #how may snowflakes at a time (= per row)

MIN_LENGTH = 1 #minimum leg length
MAX_LENGTH = 6 #maximum leg length

INV = -1 #number for invalid entries

S_SNOWFLAKE = [W_FLAKE, L_FLAKE] #size of snowflake array


# %%
# FUNCTIONS
# =========

def are_arrays_equal(a_repeat,a2):
    '''This function is the heart of the array comparer. 2 methods:
        
    METHOD 1: ROLLING THE ARRAY
    ===========================
    1) Finds all instances of item 0 of 'compared' array in 'repeated' array
       compared = [1 7 5]     repeated = [4 5 1 1 7 5 1]
       compared[0] = 1, found in instances [2 3 6]
       Current answer: [2 3 6]

    2) Once it finds them, it rolls the repeated array one step back
       repeated = [5 1 1 7 5 1 4]
    
    3) Asks if next index holds the next equality; is it equal to the
       next item in the list), and so on, until all indices of the array are done
       compared[1] = 7, found in instance [3] of the ROLLED array
       
    4) Roll the repeated array one step again
       repeated = [1 1 7 5 1 4 5]
       
    5) Is next item in comapred list equal the next item in repeated list?
       compared[2] = 5, found in instance [3 6] of the ROLLED array
       
    6) Answers so far:
       [2 3 6]
       [3]
       [3 6]
       The common element in these is 3. This function results in a non-empty
       array, so the compared array exists in the repeated array
       Differently said, the initial arrays a1 and a2 are identical
       
       
    METHOD 2: CONVERTING TO SETS
    ============================
    1) Finds all instances of item 0 of 'compared' array in 'repeated' array
       compared = [1 7 5]     repeated = [4 5 1 1 7 5 1]
       compared[0] = 1, found in instance [2 3 6]
    
    2) Finds all instances of item 1 of 'compared' array in 'repeated' array
       compared = [1 7 5]     repeated = [4 5 1 1 7 5 1]
       compared[1] = 7, found in instance [4]
       Remove 1 from the answer to account for the move in step, answer becomes [3]
         ...
    '''
    # comparer = np.where((        a_repeat == a2[0])
    #               & (np.roll(a_repeat,-1) == a2[1]) 
    #               & (np.roll(a_repeat,-2) == a2[2])
    #               & (np.roll(a_repeat,-3) == a2[3])
    #               & (np.roll(a_repeat,-4) == a2[4])
    #               & (np.roll(a_repeat,-5) == a2[5])   )[0]

    # For the following, no need to consider the wraparound effect, since 
    # duplicating the array solves the need to wraparound the array
    ans1 = np.where( a_repeat == a2[0]) [0]
    ans2 = np.where( a_repeat == a2[1]) [0] -1 #remove 1 from array since we are moving 1 step
    
    comparer_test = set(ans1) & set(ans2) #if there is no match from step 2, break
    if len(comparer_test) == 0: #if the match array has length 0 means it's empty
        return set()
    
    ans3 = np.where( a_repeat == a2[2]) [0] -2
    ans4 = np.where( a_repeat == a2[3]) [0] -3
    ans5 = np.where( a_repeat == a2[4]) [0] -4
    ans6 = np.where( a_repeat == a2[5]) [0] -5
    
    comparer = set(ans1) & set(ans2) & set(ans3) & set(ans4) & set(ans5) & set(ans6)
    # to see if the arrays have a common value, convert them to sets; this allows to compare arrays of different lenghts
    
    print(comparer, type(comparer))
    return comparer


def array_processor(a1, a2):
    '''This function aims to compare 2 numpy arrays. There are 4 ways to do so:
    1) Forward:             [1 2 3 4] = [1 2 3 4]
    2) Forward wraparoud:   [1 2 3 4] = [3 4 1 2]
    3) Backward:            [1 2 3 4] = [4 3 2 1]
    4) Backward wraparound: [1 2 3 4] = [2 1 4 3]

    By repeating the first array to [1 2 3 4 1 2 3 4], we reduce the number of 
    solutions to 2, 1) forward + wraparound, and 2) backward + wraparound:
    1) Find directly:     [3 4 1 2] in [1 2 3 4 1 2 3 4] ... YES
    2) Find flipped:  flip[2 1 4 3] in [1 2 3 4 1 2 3 4] ... YES
    
    This method eliminates two direct comparisons
    
    Input:  Arrays to compare
    Output: 1 (arrays are the same), 0 (arrays are not the same)
    '''
    
    REP = 2 #number of times to repeat/tile the array. 2 is more than enough
    a_repeat = np.tile(a1, REP) #repeat the first input array
    
    # Forward comparison
    comparer_fwd = are_arrays_equal(a_repeat,a2) #try forward comparison first
    if comparer_fwd: #if 'comparer' is not empty ==> arrays are the same
        return 1
    
    # Backward comparison
    comparer_bwd = are_arrays_equal(a_repeat, np.flip(a2)) #try backward comparison second
    if comparer_bwd:
        return 1

    return 0 #arrays are not the same


# %%
# CODE
# ====

# Generating N snowflakes of random lengths
snowflakes_array = np.empty([N_FLAKE, L_FLAKE]) #empty [N, 6] array
for i in range(N_FLAKE):
    snowflakes_array[i,:] = np.random.randint(MIN_LENGTH, MAX_LENGTH+1, S_SNOWFLAKE) #generates snowflake leg lengths


# Getting frequency of snowflake perimeters
perimeter_array = np.sum(snowflakes_array, axis=1) #sum legs of each snowflake
perimeter_freq = Counter(perimeter_array).most_common() #(most frequent, frequency) tuple


# Make array to store the indices of different perimeters
different_perimeters = len(perimeter_freq) #how many unique perimeters are there
highest_perimeter = perimeter_freq[0][1] #maximum perimeter is found on index 0 of the perimeter list from Couter().most_common()
index_perimeter = INV * np.ones([different_perimeters, highest_perimeter] ) #table showing different indices of different perimeters. set to -1 to know when the array is over

# Loop through the frequency of appearance of the sum
for i in range(len(perimeter_freq)):
    index_locator = np.where(perimeter_array == perimeter_freq[i][0]) #gives indices of snowflakes who share the same perimeter of this iteration
    for j in index_locator:
        index_perimeter[i, 0:len(j)] = j


# Cluster same-perimeter flakes together
# Table shape: [perimeter_array, real_idx, - - - - - - ]
same_perimeters = np.zeros( [N_FLAKE, L_FLAKE+2] ) #table showing different indices of different perimeters. set to -1 to know when the array is over
counter = 0
for idx,val in enumerate(index_perimeter):
    for j in val:
        if j > INV:
            same_perimeters[counter, 0] = perimeter_array[int(j)] #perimeter
            # same_perimeters[counter, 1] = j #index of snowflake
            same_perimeters[counter, 2:L_FLAKE+2] = snowflakes_array[int(j), :] #legs
            counter += 1

# Add indices column into array
idx_perimeter = index_perimeter[index_perimeter != INV] #removes invalid entries + flattens array
same_perimeters[:, 1] = idx_perimeter #index of snowflake
print(same_perimeters)

# Create array that tells when the perimeter changed
diff_perimeter   = np.diff(same_perimeters[:,0] , axis=0) #get change in perimeter
didPerimeterChange = np.where(diff_perimeter != 0, 1, diff_perimeter) #make change in perimeter binary (0=no change,1=change)
change_indices   = np.insert(didPerimeterChange, 0, 1) #add a 1 in first spot in array to consider first entry (diff function subtracts values from each other, so need to add the first value back)
print(change_indices)

# Create array of unique perimeters, to be used as reference for comparison
counter = 0
unique = np.zeros( [np.count_nonzero(change_indices), L_FLAKE+2] )
for i, val in enumerate(change_indices):
    if change_indices[i] == 1:
        unique[counter] = same_perimeters[i]
        counter += 1
# print(unique)
individual_perimeter = len(unique) #unique perimeters


# Compare snowflakes of same perimeter
equal_snowflakes = INV*np.ones( [np.count_nonzero(change_indices), int(perimeter_freq[0][1]) ] ) #array of shape [unique perimeters, freq of most common perimeter], we are overestimating by a lot
counter = 0
for ind, val in enumerate(same_perimeters):
    isequal = array_processor(same_perimeters[ind,2:], same_perimeters[ind+1,2:])


    counter += 1
    if counter > individual_perimeter:
        break

#     if change_indices[ind] == 1:
#         print(change_indices[ind], val[1])

