# Performs bubble sort algorithms

def insertsort(array): # straight insert sorting
    for j in range(1, len(array)):
        k = array[j] # k = key / temp
        i = j - 1
        while i >= 0 and k < array[i]:
            array[i + 1] = array[i]
            i -= 1
        array[i + 1] = k
    return array

def binary_insertsort(array): # incorporates binary search
    def withinRange(x):
        if x < 0: return 0
        elif x == len(array): x-=1
        else: return x
    def binarysearch(begin, k, end):
        mid = ( (begin := withinRange(begin)) + (end:=withinRange(end)) ) // 2
        if begin == end:
            return mid
        if k > array[mid]: # rightmost
            mid = binarysearch(mid + 1, k, end)
        else: # mid + leftmost
            mid = binarysearch(begin, k, mid)
        return mid
    for j in range(1, len(array)):
        k = array[j] # k = key / temp
        i = binarysearch(0, k, j)
        array.insert(i, array.pop(j))
    return array

def twoway_insertsort(array): # bidirectional insert sorting
    array, c, stack = array[-1:], array.pop(), array
    while stack:
        i = array.index(c) # c = center
        k = stack.pop() # k = key / temp
        if k < c: # left insertion
            array.insert(i, k)
            while i > 0 and k < array[i - 1]:
                array[i] = array[i - 1]
                i -= 1
            array[i] = k
        elif k > c: # right insertion
            array.insert(i + 1, k)
            i += 1
            while i < len(array) - 1 and k > array[i + 1]:
                array[i] = array[i + 1]
                i += 1
            array[i] = k
        else: # k == c
            array.insert(i, k)
    return array
    
def shellsort():
    return

list = [10, 8, 13, 17, 5, 2, 9, 6, 20, 18, 4, 3,11,15,14,19, 1,12, 7,16]
print(binary_insertsort(list))