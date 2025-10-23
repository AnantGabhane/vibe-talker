def binary_search(list_name, target):
    low = 0
    high = len(list_name) - 1

    while low <= high:
        mid = (low + high) // 2
        if list_name[mid] == target:
            return mid
        elif list_name[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1

# Example usage:
my_list = [2, 5, 7, 8, 11, 12]
target = 13
index = binary_search(my_list, target)

if index != -1:
    print(f'Target {target} found at index {index}')
else:
    print(f'Target {target} not found in the list')
