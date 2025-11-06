
odd = [1, 2, 3, 3, 4, 5, 5, 6, 7, 7, 7, 8, 9]
even = [1, 2, 2, 2, 2, 2, 3, 4, 5, 6, 7, 8, 8, 8]

def occurences(values: list[int], target: int) -> int:
    '''
    method to accept a sorted list of integer vales and return
    how many times the target value appears on the list using
    binary search. uses the two functions to check where the start
    and end of the target cluster is. then returns the difference
    to show how many there are.
    '''
    occurence = 0

    left_occur = left_index(values, target)  # start of occurence cluster
    right_occur = right_index(values, target)  # end of occurence cluster

    if (right_occur == -1) and (left_occur == -1):  # to account for the adding 1
        occurence = 0
    else:
        occurence = right_occur - left_occur + 1  # subtract start cluster from end and add one for overlap

    return occurence


def left_index(values: list[int], target: int) -> int:
    '''
    function to look at the left array and see if target is in the middle
    if target is found, array keeps looking at left neighbor. if
    middle value is too small it'll move towards right (larger numbers)
    if middle value too large it'll move towards left (smaller numbers)
    returns the index that we want to look at next
    '''
    small = 0
    large = len(values) - 1
    left_neighbor = -1 
    while (small <= large):  # and (count >= 0):
        middle = (small + large) // 2
        if values[middle] == target:  # found target
            left_neighbor = middle
            large = middle - 1  # look left neighbor (smaller value)
        elif values[middle] < target:
            small = middle + 1  # move towards right, values too little
        else: #values[middle] > target:
            large = middle - 1  # move towards left, values too much
    return left_neighbor

def right_index(values: list[int], target: int) -> int:
    '''
    function to look at right array and return the index
    of the found target. uses a while loop to check if middle
    index has our value, if not it keeps moving index and checking
    returns the right neighbor of the target value
    '''
    small = 0
    large = len(values) - 1
    right_neighbor = -1
    while (small <= large):
        middle = (small + large) // 2
        if values[middle] == target:
            right_neighbor = middle
            small = middle + 1  # look right neighbor
        elif values[middle] < target:
            small = middle + 1  # we are looking to small, move right towards larger
        else:  # values[middle] > target:
            large = middle - 1  #values too high, move towards left smaller numbers
    return right_neighbor

def main():
    '''
    main function for testing the code. tests function
    occurance with the two arrays even and odd
    '''
    print("odd length", len(odd))
    print("even length",len(even))
    print(f"\noccurence of 10 odd (not found) -> {occurences(odd, 10)}")
    print(f"occurence of 10 even (not found) -> {occurences(even, 10)}")
    print(f"\noccurence of 7 odd (expected 3) -> {occurences(odd, 7)}")
    print(f"occurence of 2 even (expected 5) -> {occurences(even, 2)}")
    print(f"occurence of 4 odd (expected 1) -> {occurences(odd, 4)}")
    print(f"occurence of 4 even (expected 1) -> {occurences(even, 4)}")

main()


