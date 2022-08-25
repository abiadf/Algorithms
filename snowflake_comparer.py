# -*- coding: utf-8 -*-
"""
@author: Fouad
"""

import numpy as np
from collections import Counter

# %%
# CONSTANTS
# =========

N_FLAKE = int(1e3) #number of snowflakes to compare

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
    if comparer_bwd: #if 'comparer' is not empty ==> arrays are the same
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
perimeter_list = np.sum(snowflakes_array, axis=1) #sum legs of each snowflake
perimeter_freq = Counter(perimeter_list).most_common() #(most frequent, frequency) tuple


# Make array to store the indices of different perimeters
different_perimeters   = len(perimeter_freq) #how many unique perimeters are there
mostCommonPerimeterFreq= perimeter_freq[0][1] #maximum perimeter is found on index 0 of the perimeter list from Couter().most_common()
index_perimeter        = INV * np.ones([different_perimeters, mostCommonPerimeterFreq] ) #table showing different indices of different perimeters. set to -1 to know when the array is over

# Loop through the frequency of appearance of the sum
for i in range(len(perimeter_freq)):
    index_locator = np.where(perimeter_list == perimeter_freq[i][0]) #gives indices of snowflakes who share the same perimeter of this iteration
    for j in index_locator:
        index_perimeter[i, 0:len(j)] = j


# Cluster same-perimeter flakes together
# Table shape: [perimeter_list, real_idx, - - - - - - ]
snowflakesByPerimeter = np.zeros( [N_FLAKE, L_FLAKE+2] ) #table showing different indices of different perimeters. set to -1 to know when the array is over
counter = 0
for idx,val in enumerate(index_perimeter):
    for j in val:
        if j > INV:
            snowflakesByPerimeter[counter, 0] = perimeter_list[int(j)] #perimeter
            # snowflakesByPerimeter[counter, 1] = j #index of snowflake
            snowflakesByPerimeter[counter, 2:L_FLAKE+2] = snowflakes_array[int(j), :] #legs
            counter += 1


# Add indices column into array
perimetersIndexByFreq = index_perimeter[index_perimeter != INV] #removes invalid entries + flattens array
snowflakesByPerimeter[:, 1] = perimetersIndexByFreq #index of snowflake
# print(snowflakesByPerimeter)


# Create array that tells when the perimeter changed
perimeterDiff = np.diff(snowflakesByPerimeter[:,0] , axis=0) #get change in perimeter
didPerimeterChange = np.where(perimeterDiff != 0, 1, perimeterDiff) #make change in perimeter binary (0=no change,1=change)
changedPerimeterIndices = np.insert(didPerimeterChange, 0, 1) #add a 1 in first spot in array to consider first entry (diff function subtracts values from each other, so need to add the first value back)


# Create array of unique perimeters, to be used as reference for comparison
counter = 0
uniquePerimetersArray = np.zeros( [different_perimeters, L_FLAKE+2] )
for i, val in enumerate(changedPerimeterIndices):
    if changedPerimeterIndices[i] == 1:
        uniquePerimetersArray[counter] = snowflakesByPerimeter[i]
        counter += 1


# Compare snowflakes of same perimeter
sfOfSamePerimeter = INV*np.ones( [different_perimeters, mostCommonPerimeterFreq] ) #array of shape [unique perimeters, freq of most common perimeter], we are overestimating by a lot
withPerimeter = np.insert(sfOfSamePerimeter, 0, uniquePerimetersArray[:,0], axis=1)
counter = 0


# setting the 1st entry as ref values
referenceP   = snowflakesByPerimeter[0][0]  #perimeter
referenceIdx = snowflakesByPerimeter[0][1]  #index
referenceSF  = snowflakesByPerimeter[0][2:] #snowflake legs

for ind, val in enumerate(snowflakesByPerimeter[1:]): #start from 2nd value because 1st was used as ref in above lines
    
    # Compare snowflakes with the 1st one in its cluster - WITHOUT LOOPING
    if (ind != N_FLAKE-1 ): #if we are NOT on the last snowflake
        if (referenceP != snowflakesByPerimeter[ind][0]): #if the reference perimeter changed, then the cluster changed (since cluster is based on the perimeter)
            referenceP  = snowflakesByPerimeter[ind][0]   #change ref. perimeter
            referenceIdx= snowflakesByPerimeter[ind][1]   #change ref. index
            referenceSF = snowflakesByPerimeter[ind][2:]  #change ref. snowflake
            continue #if the ref changed, SKIP to next loop (otherwise will compare ref with itself)

        # # To see where the snowflake changed perimeter
        # if (snowflakesByPerimeter[ind][0] != snowflakesByPerimeter[ind-1][0] ):
        #     print('P change @ idx: ', val[1])

    a_ref  = referenceSF #the repeated array
    a_2    = snowflakesByPerimeter[ind, 2:] #the reference array
    isEqual= array_processor(a_ref, a_2)

    if isEqual:
        desiredPerimeter = np.where(withPerimeter[:,0] == snowflakesByPerimeter[ind,0]) #for what perimeter value is this the case?
        desiredPerimeterValue = desiredPerimeter[0][0] #keeps the int value
        
        # following line NOT working :(
        withPerimeter[desiredPerimeterValue][(withPerimeter[desiredPerimeterValue] == -1).nonzero()[0][:1]] = snowflakesByPerimeter[ind,1]
        # https://stackoverflow.com/questions/35016737/how-to-replace-only-the-first-n-elements-in-a-numpy-array-that-are-larger-than-a

    # if ind+1 == len(snowflakesByPerimeter)-1: #if index reaches penultimate row
    #     break


# Remove rows from 'withPerimeter' without similar snowflakes (=validEntries)
invalidEntriesCrit = INV*np.shape(withPerimeter)[1] + 1
validEntries = np.zeros( [0, np.shape(withPerimeter)[1] ] ) #want it of fixed width, but unknown length (so set to 0)
for i, val in enumerate(withPerimeter):
    if np.sum(withPerimeter[i,1:]) > invalidEntriesCrit: #invalid entries are -1, so the sum of the row will be negative
        validEntries = np.vstack([validEntries, val]) #we have a match


# Find which snowflake shape has the most members
numberOfEntries = np.empty( [len(validEntries), 1] ) # the width is 1 cause for each array, we just need the number of similar snowflakes
for i,val in enumerate(validEntries):
    numberOfEntries[i] = np.where(validEntries[i]==INV)[0][0] -1  # finds first instance of the similarity array NOT being similar. Removes 1 because we want to remove the perimeter and keep valid entries 
highestNumber = int( np.max(numberOfEntries) ) #how many identical snowflakes (in the cluster with the highest number of identical snowflakes)


# Keep equal snowflakes
cleaned = np.delete(validEntries, np.s_[highestNumber+1:], axis=1) #removes all columns after the last valid one
EqualSnowflakes = cleaned[:, 1:] #removes 1st column (= perimeter)
print(EqualSnowflakes) 


