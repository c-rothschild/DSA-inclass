
# making insertion sort
def insertion_sort(arr):
    # 1. Iterate through each item in the array, starting with item at index 1 (i)
    for i in range(1, len(arr)): 
        # 2. set comparison index to i - 1 (comp)
        comp = i - 1
        # 3. while comparison index isn't 0, keep looping
        while comp >= 0:
            # if item is greater than item at comparison index, break from loop
            if arr[i] > arr[comp]:
                break
            comp -=1
        # if comparison + 1 equals len(arr) - 1, return
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
