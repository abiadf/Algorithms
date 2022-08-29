# -*- coding: utf-8 -*-
"""
@author: Fouad
"""

import numpy as np
from collections import Counter

from functions import are_arrays_equal, array_processor

# %%
# CONSTANTS
# =========

N_FLAKE = int(1e4) #number of snowflakes to compare

L_FLAKE = 6 #how many legs in a snowflake
W_FLAKE = 1 #how may snowflakes at a time (= per row)

MIN_LENGTH = 1 #minimum leg length
MAX_LENGTH = 8 #maximum leg length

INV = -1 #number for invalid entries

S_SNOWFLAKE = [W_FLAKE, L_FLAKE] #size of snowflake array


# %%
# CODE
# ====

# Make all numbers appear as INT and not FLOAT
np.set_printoptions(suppress = True)

def snowflake_generator(N_FLAKE, L_FLAKE):
    # Generating N snowflakes of random lengths
    snowflakes = np.empty([N_FLAKE, L_FLAKE]) #empty [N, 6] array
    for i in range(N_FLAKE):
        snowflakes[i,:] = np.random.randint(MIN_LENGTH, MAX_LENGTH+1, S_SNOWFLAKE) #generates snowflake leg lengths
    return snowflakes


def perimeter_array(snowflakes):
    # Getting frequency of snowflake perimeters
    perimeter_list = np.sum(snowflakes, axis=1) #sum legs of each snowflake
    perimeter_freq = Counter(perimeter_list).most_common() #(most frequent, frequency) tuple
    
    # Make array to store the indices of different perimeters
    different_perimeters   = len(perimeter_freq) #how many unique perimeters are there
    mostCommonPerimeterFreq= perimeter_freq[0][1] #maximum perimeter is found on index 0 of the perimeter list from Couter().most_common()
    index_perimeter        = INV * np.ones([different_perimeters, mostCommonPerimeterFreq] ) #table showing different indices of different perimeters. set to -1 to know when the array is over

    return perimeter_list, perimeter_freq, different_perimeters, \
        mostCommonPerimeterFreq, index_perimeter



def sf_by_perimeter(perimeter_list, perimeter_freq, index_perimeter, snowflakes):
    # Loop through the frequency of appearance of the sum
    for i in range(len(perimeter_freq)):
        index_locator = np.where(perimeter_list == perimeter_freq[i][0]) #gives indices of snowflakes who share the same perimeter of this iteration
        for j in index_locator:
            index_perimeter[i, 0:len(j)] = j

    # Cluster same-perimeter flakes together
    # Table shape: [perimeter_list, real_idx, - - - - - - ]
    sfByPerimeter = np.zeros( [N_FLAKE, L_FLAKE+2] ) #table showing different indices of different perimeters. set to -1 to know when the array is over
    counter = 0
    for idx,val in enumerate(index_perimeter):
        for j in val:
            if j > INV:
                sfByPerimeter[counter, 0] = perimeter_list[int(j)] #perimeter
                # sfByPerimeter[counter, 1] = j #index of snowflake
                sfByPerimeter[counter, 2:L_FLAKE+2] = snowflakes[int(j), :] #legs
                counter += 1

    return sfByPerimeter



def unique_perimeters(index_perimeter, sfByPerimeter, different_perimeters):
    # Add indices column into array
    perimetersIndexByFreq = index_perimeter[index_perimeter != INV] #removes invalid entries + flattens array
    sfByPerimeter[:, 1] = perimetersIndexByFreq #index of snowflake
    
    # Create array that tells when the perimeter changed
    perimeterDiff = np.diff(sfByPerimeter[:,0] , axis=0) #get change in perimeter
    didPerimeterChange = np.where(perimeterDiff != 0, 1, perimeterDiff) #make change in perimeter binary (0=no change,1=change)
    changedPerimeterIndices = np.insert(didPerimeterChange, 0, 1) #add a 1 in first spot in array to consider first entry (diff function subtracts values from each other, so need to add the first value back)
    
    # Create array of unique perimeters, to be used as reference for comparison
    counter = 0
    uniquePerimetersArray = np.zeros( [different_perimeters, L_FLAKE+2] )
    for i, val in enumerate(changedPerimeterIndices):
        if changedPerimeterIndices[i] == 1:
            uniquePerimetersArray[counter] = sfByPerimeter[i]
            counter += 1
    
    return uniquePerimetersArray


def reference_values(different_perimeters, mostCommonPerimeterFreq, \
                     uniquePerimetersArray, sfByPerimeter):
    
    # setting the 1st entry as ref values
    referenceP   = sfByPerimeter[0][0]  #perimeter
    referenceIdx = sfByPerimeter[0][1]  #index
    referenceSF  = sfByPerimeter[0][2:] #snowflake legs

    return referenceP, referenceIdx, referenceSF


def finding_equal_sf(different_perimeters, mostCommonPerimeterFreq, \
                     uniquePerimetersArray, sfByPerimeter, referenceP, \
                     referenceIdx, referenceSF ):

    # Compare snowflakes of same perimeter
    sfOfSamePerimeter = INV*np.ones( [different_perimeters, mostCommonPerimeterFreq] ) #array of shape [unique perimeters, freq of most common perimeter], we are overestimating by a lot
    sfWithPerimeter = np.insert(sfOfSamePerimeter, 0, uniquePerimetersArray[:,0], axis=1)

    for ind, val in enumerate(sfByPerimeter[1:]): #start from 2nd value because 1st was used as ref in above lines
        # Compare snowflakes with 1st one in its cluster - WITHOUT LOOPING
        if (ind != N_FLAKE-1 ): #if we are NOT on the last snowflake
            if (referenceP != sfByPerimeter[ind][0]): #if the reference perimeter changed, then the cluster changed (since cluster is based on the perimeter)
                referenceP  = sfByPerimeter[ind][0]   #change ref. perimeter
                referenceIdx= sfByPerimeter[ind][1]   #change ref. index
                referenceSF = sfByPerimeter[ind][2:]  #change ref. snowflake
                continue #if the ref changed, SKIP to next loop (otherwise will compare ref with itself)
    
            # # Find where the snowflake changed perimeter:
            # if (sfByPerimeter[ind][0] != sfByPerimeter[ind-1][0] ):
            #     print('P change @ idx: ', val[1])
    
        a_ref  = referenceSF            # repeated array
        a_2    = sfByPerimeter[ind, 2:] # the reference array
        isEqual= array_processor(a_ref, a_2)
    
        if isEqual:
            desiredPerimeter = np.where(sfWithPerimeter[:,0] == sfByPerimeter[ind,0]) #for what perimeter value is this the case?
            desiredPerimeterValue = desiredPerimeter[0][0] #keeps the int value
            
            sfWithPerimeter[desiredPerimeterValue][(sfWithPerimeter[desiredPerimeterValue] == INV).nonzero()[0][:1]] = sfByPerimeter[ind,1] # replacing the first elements in array that are = -1
            # https://stackoverflow.com/questions/35016737/how-to-replace-only-the-first-n-elements-in-a-numpy-array-that-are-larger-than-a
            
            loc = np.where(sfWithPerimeter[desiredPerimeterValue] == INV)[0][0] #where is the first -1 (so we can replace it with the ref index)?
            if referenceIdx not in sfWithPerimeter[desiredPerimeterValue]: #if reference index is NOT in SF array, add it
                sfWithPerimeter[desiredPerimeterValue][loc] = referenceIdx # insert reference index into SF array
            
    return sfWithPerimeter
            
            
def remove_nonunique_sf(sfWithPerimeter):
    # Remove rows from 'sfWithPerimeter' without similar snowflakes (=validEntries)
    invalidEntriesCrit = INV*np.shape(sfWithPerimeter)[1] + 1
    validEntries = np.zeros( [0, np.shape(sfWithPerimeter)[1] ] ) #want it of fixed width, but unknown length (so set to 0)
    for i, val in enumerate(sfWithPerimeter):
        if np.sum(sfWithPerimeter[i,1:]) > invalidEntriesCrit: #invalid entries are -1, so the sum of the row will be negative
            validEntries = np.vstack([validEntries, val]) #we have a match, add values vertically into array

    return validEntries


def sf_with_most_members(validEntries):
    # Find which snowflake shape has the most members
    numberOfEntries = np.empty( [len(validEntries), 1] ) # the width is 1 cause for each array, we just need the number of similar snowflakes
    for i, val in enumerate(validEntries):
        numberOfEntries[i] = np.where(validEntries[i]==INV)[0][0] -1  # finds first instance of the similarity array NOT being similar. Removes 1 because we want to remove the perimeter and keep valid entries 
    
    highestNumber = int( np.max(numberOfEntries) ) #how many identical snowflakes (in the cluster with the highest number of identical snowflakes)

    return highestNumber


def equal_snowflakes(highestNumber, validEntries):
    # Keep equal snowflakes
    cleaned = np.delete(validEntries, np.s_[highestNumber+1:], axis=1) #removes all columns after the last valid one
    EqualSnowflakes = cleaned[:, 1:] #removes 1st column (= perimeter)

    return EqualSnowflakes



# %% Running the code

snowflakes = snowflake_generator(N_FLAKE, L_FLAKE)

perimeter_list, perimeter_freq, different_perimeters, \
    mostCommonPerimeterFreq, index_perimeter = perimeter_array(snowflakes)

sfByPerimeter = sf_by_perimeter(perimeter_list, perimeter_freq, index_perimeter, snowflakes)

uniquePerimetersArray = unique_perimeters(index_perimeter, sfByPerimeter, \
                                          different_perimeters)

referenceP, referenceIdx, referenceSF = reference_values(different_perimeters, \
                                                         mostCommonPerimeterFreq, \
                                                         uniquePerimetersArray, sfByPerimeter)

sfWithPerimeter = finding_equal_sf(different_perimeters, mostCommonPerimeterFreq, \
                     uniquePerimetersArray, sfByPerimeter, referenceP, \
                     referenceIdx, referenceSF)

validEntries = remove_nonunique_sf(sfWithPerimeter)

highestNumber = sf_with_most_members(validEntries)    

EqualSnowflakes = equal_snowflakes(highestNumber, validEntries)
    

print(EqualSnowflakes)

