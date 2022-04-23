# Reusable functions/procedures

# Python library imports
import os
import ssl
import sys
import math
import time
import argparse
import datetime

# Check if an item is in list
# Requires a list and item to be searched
# Returns True if item is in list, False otherwise
def isInArr(arr,val):
    for item in arr:
        if val == item:
            return True
    return False
# Alternate version to search within list of lists
# Requires inner-index to be searched
def isInArrofArr(arr,val,index):
    for item in arr:
        if val == item[index]:
            return True
    return False

# Check array length
# Requires a list
# Returns list length
def arrLen(arr):
    i = 0
    for items in arr:
        i += 1
    return i

# Get index-limited array maximum
# Requires a list of lists, starting outer-index, and searching inner-index
# Returns maximum value of the inner-index within range starting from starting outer-index until end of list, and its index number
def get_max(arr, index_start, search_index):
    max = int(arr[index_start][search_index])
    maxId = index_start
    for i in range (index_start,arrLen(arr)):
        if int(arr[i][search_index]) > max:
            max = int(arr[i][search_index])
            maxId = i
    return (str(max),maxId)

# Get index-limited array minimum
# Requires a list of lists, starting outer-index, and searching inner-index
# Returns minimum value of the inner-index within range starting from starting outer-index until end of list and its index number
def get_min(arr, index_start, search_index):
    min = int(arr[index_start][search_index])
    minId = index_start
    for i in range (index_start,arrLen(arr)):
        if int(arr[i][search_index]) < min:
            min = int(arr[i][search_index])
            minId = i
    return (str(min),minId)

# Check list of list item index
# Requires a list of lists, value to be searched, inner-index of the value
# Returns outer-index number
def get_idx(arr, val, j):
   for i in range (arrLen(arr)):
       if arr[i][j] == val:
           return i

# Array item swap
# Requires a list and two array index numbers
# Returns the list with items of the two index numbers having switched places
def swap(array, indeks_1, indeks_2):
  Temp = array[indeks_1]
  array[indeks_1] = array[indeks_2]
  array[indeks_2] = Temp
  return array

# Array sorting function
# Requires list of lists to be sorted, sorting inner-index, and ascending/descending option
# Returns sorted list
def arrSort(arr,index,asc=True):
    for i in range(arrLen(arr)):
        # Get minimum/maximum (critical) value index
        if asc:
            valId = get_min(arr,i,index)[1]
        else:
            valId = get_max(arr,i,index)[1]
        # Get critical value index
        # valId = get_idx(arr, val, index)
        # Put critical value in current iterated outer-index (swap positions)
        arr = swap(arr, i, valId)
    return arr

# Line-by-line text parsing function
# Requires file path input, fileLoc; and column separator character, colSeparator
# Returns table array
def table_parse(fileLoc, colSeparator):
    f = open(fileLoc, "r") # Initialize file object
    f.readline() # Ignore first line
    mainArr = [] # Init main table list
    rows = f.readlines() # get all table rows
    i = 0
    # Iterate all rows
    for row in rows:
        rows[i] = row.rstrip() # Remove trailing newline
        rowArr = [] # Init row array of columns
        colData = "" # Init column data
        for char in rows[i]: # Iterate all characters in a row for parsing
            if char == colSeparator: # On finding separator character, insert column data to current row array & continue parsing next column
                rowArr += [colData]
                colData = "" # Reinit column data
            else:
                colData += char
        rowArr += [colData]
        i += 1
        mainArr += [rowArr] # Insert row array in main table list
    f.close()
    return mainArr

# ID Generator
# Requires a list of lists and ID inner-index
# Return a new ID number -> Returned value is the smallest integer possible higher than the biggest integer in list
def generateID(arr,index):
    maxId = get_max(arr,0,index)[0]
    return int(maxId) + 1

# Convert python array to csv table
# Requires folder path, array to be converted, first-line header (table headers), column separator, and line separator
# Does not return any specific value
def array_to_csv(loc,arr,header,column,newline):
  if os.path.exists(loc): # Remove file if already exists
    os.remove(loc)
  f = open(loc, "w") # Init file object
  out = header + newline # Add csv table headers
  for row in arr:
    for j in range(arrLen(row)):
      out += row[j] # add a column
      if j < arrLen(row)-1:
        out += column # add column separator
    out += newline # add line separator
  f.write(out) # Write to csv file
  f.close()
  return True

# Array filtering function
# Requires a list of lists to be filtered, and a list of filter arrays
# filter array -> array that contains value to be searched, and searching inner-index -> Example: ["duar", 8]
# Returns a list of the matching results' indices in input array
def arrFilter(arr,filters):
    result = [] # Output initialization
    for item in arr:
        match = True # Initialization
        for criteria in filters:
            if criteria[0] != item[criteria[1]]:
                match = False
                break # One criteria not fulfilled, continue searching next item in arr
        if match:
            result += [get_idx(arr,item[0],0)]
    return result