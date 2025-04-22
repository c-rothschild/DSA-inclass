import random
def random_number_list(n):
    rand_list = []
    for _ in range(n):
        rand_list.append(random.randint(-1000, 1000))
    return rand_list

# create a merge helper function
def merge(arr, start, mid, end):
    comparisons = 0
    # Create temporary arrays
    left = arr[start:mid]
    right = arr[mid:end]
    
    # Merge back into the original array
    i = j = 0
    k = start
    
    
    while i < len(left) and j < len(right):
        comparisons += 2
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    comparisons += 1
    
    # Copy remaining elements if any
    while i < len(left):
        comparisons += 1
        arr[k] = left[i]
        i += 1
        k += 1
    comparisons += 1
        
    while j < len(right):
        comparisons += 1
        arr[k] = right[j]
        j += 1
        k += 1
    comparisons += 1
    return comparisons

def merge_sort(arr, start=0, end=None):
    comparisons = 0
    comparisons += 1
    if end is None:
        end = len(arr)
        
    # Base case: arrays with 0 or 1 elements are already sorted
    comparisons += 1
    if end - start <= 1:
        return comparisons
        
    # Find the middle point
    mid = (start + end) // 2
    
    # Sort first and second halves
    comparisons += merge_sort(arr, start, mid)
    comparisons += merge_sort(arr, mid, end)
    
    # Merge the sorted halves
    comparisons += merge(arr, start, mid, end)
    return comparisons


# making insertion sort
def insertion_sort(arr):
    comparisons = 0
    # 1. Iterate through each item in the array, starting with item at index 1 (i)
    for i in range(1, len(arr)): 
        # 2. set comparison index to i - 1 (comp)
        comp = i - 1
        # 3. while comparison index isn't 0, keep looping
        while comp >= 0:
            # if item is greater than item at comparison index, break from loop
            comparisons+=1
            if arr[i] > arr[comp]:
                break
        
            comp -=1
        # if comparison + 1 equals len(arr) - 1, return
        comparisons += 1
        if comp + 1 == len(arr) + 1:
            return 
        # set variable item to arr[i].pop
        item = arr.pop(i)
        # get a subarry from arr from indices comp + 1 to len(arr) - 1
        subArr = arr[comp + 1: len(arr)]
        # delete that subarray from arr
        del arr[comp + 1: len(arr) ]
        # arr = arr + [item] + subarray
        arr[comp+1:comp+1] = [item] + subArr
    return comparisons

