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
    if len(array) > 1:
        mid1 = len(array) // 3
        mid2 = mid1 * 2
        left_part = array[:mid1]
        mid_part = array[mid1:mid2]
        right_part = array[mid2:]

        three_way_mergesort(left_part)
        three_way_mergesort(mid_part)
        three_way_mergesort(right_part)

        i = j = k = l = 0

        while i < len(left_part) and j < len(mid_part) and k < len(right_part):
            if left_part[i] < mid_part[j]:
                if left_part[i] < right_part[k]:
                    array[l] = left_part[i]
                    i += 1
                else:
                    array[l] = right_part[k]
                    k += 1
            else:
                if mid_part[j] < right_part[k]:
                    array[l] = mid_part[j]
                    j += 1
                else:
                    array[l] = right_part[k]
                    k += 1
            l += 1

        while i < len(left_part) and j < len(mid_part):
            if left_part[i] < mid_part[j]:
                array[l] = left_part[i]
                i += 1
            else:
                array[l] = mid_part[j]
                j += 1
            l += 1

        while j < len(mid_part) and k < len(right_part):
            if mid_part[j] < right_part[k]:
                array[l] = mid_part[j]
                j += 1
            else:
                array[l] = right_part[k]
                k += 1
            l += 1

        while i < len(left_part):
            array[l] = left_part[i]
            i += 1
            l += 1

        while j < len(mid_part):
            array[l] = mid_part[j]
            j += 1
            l += 1

        while k < len(right_part):
            array[l] = right_part[k]
            k += 1
            l += 1
    return array


def iterative_mergesort(array):  # bottom-up mergesort
    return array


def in_place_mergesort(array):
    return array


def natural_merge_sort(array):
    return array


def parallel_merge_sort(array):
    return array
