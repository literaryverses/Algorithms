def selectionsort(array):
    for i in range(len(array)):
        min = i
        for j in range(i + 1, len(array)):
            if array[j] < array[min]:
                min = j

        array[j], array[min] = array[min], array[j]


def heapsort(array):
    return


def bingosort(array):
    return


def cocktailsort(array):  # double selection sort
    return
