# create a merge helper function
def merge(left, right):
    result = []
    while left and right:
        if left[0] < right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    
    # Add any remaining elements
    result += left + right
    return result

def merge_sort(arr):
    # Base case: arrays with 0 or 1 elements are already sorted
    if len(arr) <= 1:
        return arr
        
    # Divide array into two halves
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    # Merge the sorted halves
    return merge(left, right)

array = [4, 3, 2, 1]
sorted_array = merge_sort(array)
print(sorted_array)
