# Performs bubble sort algorithms


def bubblesort(array):  # standard bubble sort algorithm
    n = len(array)
    for i in range(0, n - 1):
        for j in range(0, n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array


def modified_bubblesort(array):  # modified bubble sort algorithm
    n = len(array)
    for i in range(0, n - 1):
        swapped = False
        for j in range(0, n - i - 1):
            if array[j] > array[j + 1]:
                swapped = True
                array[j], array[j + 1] = array[j + 1], array[j]
        if not swapped:
            break  # quits if no swaps are made
    return array


def cocktail_shaker_sort(array):  # bidirectional bubble sort
    n = len(array)
    for i in range(0, n - 1):
        swapped = False
        for j in range(i, n - i - 1):  # left to right
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                swapped = True
        if not swapped:
            break
        swapped = False
        for k in range(n - i - 1, i + 1, -1):  # right to left
            if array[k] < array[k - 1]:
                array[k], array[k - 1] = array[k - 1], array[k]
                swapped = True
        if not swapped:
            break
    return array
