# Performs insertsort algorithms


def insertsort(array):  # straight insert sorting
    for j in range(1, len(array)):
        k = array[j]  # k = key / temp
        i = j - 1
        while i >= 0 and k < array[i]:
            array[i + 1] = array[i]
            i -= 1
        array[i + 1] = k
    return array


def binary_insertsort(array):  # incorporates binary search
    def withinRange(x):  # keeps parameters within range of array
        if x < 0:
            return 0
        elif x == len(array):
            return x - 1
        else:
            return x

    def binarysearch(begin, k, end):
        mid = ((begin := withinRange(begin)) + (end := withinRange(end))) // 2
        if begin == end:
            return mid
        if k > array[mid]:  # rightmost
            mid = binarysearch(mid + 1, k, end)
        else:  # mid + leftmost
            mid = binarysearch(begin, k, mid)
        return mid

    for j in range(1, len(array)):
        k = array[j]  # k = key / temp
        i = binarysearch(0, k, j)
        array.insert(i, array.pop(j))
    return array


def twoway_insertsort(array):  # bidirectional insert sorting
    array, c, stack = array[-1:], array.pop(), array
    while stack:
        i = array.index(c)  # c = center
        k = stack.pop()  # k = key / temp
        if k < c:  # left insertion
            array.insert(i, k)
            while i > 0 and k < array[i - 1]:
                array[i] = array[i - 1]
                i -= 1
            array[i] = k
        elif k > c:  # right insertion
            array.insert(i + 1, k)
            i += 1
            while i < len(array) - 1 and k > array[i + 1]:
                array[i] = array[i + 1]
                i += 1
            array[i] = k
        else:  # k == c
            array.insert(i, k)
    return array


def shellsort(array, seqType: str):  # Shell's algorithm
    gaps = [x := 1]
    n = len(array)

    # gap sequences
    shell_fx = lambda x: 2 ** (x - 1)
    knuth_fx = lambda x: (3**x - 1) // 2
    sedgwick_fx = lambda x: 4**x + 3 * 2 ** (x - 1) + 1

    if seqType.lower() == "shell":  # n / 2^k
        while gaps[0] <= n // 2:
            gaps.insert(0, shell_fx(x := x + 1))
    elif seqType.lower() == "knuth":  # (3^k - 1)/2
        while gaps[0] < n:
            gaps.insert(0, knuth_fx(x := x + 1))
    elif seqType.lower() == "sedgwick":  # 4^k + 3*2^(k-1) + 1
        while gaps[0] < n:
            gaps.insert(0, sedgwick_fx(x := x + 1))
    else:
        raise Exception("Not an available function")
    gaps.pop(0)  # remove since gap[0] > n

    for gap in gaps:
        for j in range(gap, n):  # elements in array, left to right
            for i in range(j, 0, -gap):  # elements in gap, right to left
                if i >= gap and array[i - gap] > array[i]:
                    array[i], array[i - gap] = (
                        array[i - gap],
                        array[i],
                    )  # bypass key via multiple assignment

    return array
