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
    def binarysearch(array, begin, k, end):
        mid = (begin + end) // 2
        if k < array[mid]:
            binarysearch(array, begin, k, mid - 1)
        elif k > array[mid]:
            binarysearch(array, mid + 1, k, end)
        else: # k == array[mid]
            return mid

def twoway_insertsort(array): # bidirectional insert sorting
    array, c, stack = array[-1:], array.pop(), array
    while stack:
        i = array.index(c)
        k = stack.pop()
        if k < c:
            array.insert(i, k)
            while i > 0 and k < array[i - 1]:
                array[i] = array[i - 1]
                i -= 1
            array[i] = k
        elif k > c:
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