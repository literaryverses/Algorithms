# Performs mergesort algorithms


def mergesort(array):
    if len(array) > 1:
        mid = len(array) // 2
        left_half = array[:mid]
        right_half = array[mid:]

        mergesort(left_half)
        mergesort(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                array[k] = left_half[i]
                i += 1
            else:
                array[k] = right_half[j]
                j += 1
            k += 1
        while i < len(left_half):
            array[k] = left_half[i]
            i += 1
            k += 1
        while j < len(right_half):
            array[k] = right_half[j]
            j += 1
            k += 1
    return array


def three_way_mergesort(array):
    return array


def in_place_mergesort(array):
    return array


def in_place_mergesort_2(array):
    return array


def merge_sort_with_O1_space(array):
    return array


def bottom_up_merge_sort(array):
    return array


def natural_merge_sort(array):
    return array


def parallel_merge_sort(array):
    return array


arr = [12, 11, 13, 5, 6, 7, 1]
mergesort(arr)
print("Sorted array:", arr)
