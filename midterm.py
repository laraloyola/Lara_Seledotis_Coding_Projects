''' clinic uses n x n waiting room in rows
new arrivals sit at first seat scanning front to back, left to right
next person called is front left seat

goal: stack only those who arrived last and who are next. use n x n grid as seating area
where the front of queue and back of queue pointer advance in row-major order (wrapping around)
'''
'''
Task 1: 
a. read and explain the data model. 
b. Explain how row-major order (front to back, left to right) using
- implemented using a 2D array (self._underlying)
- a pair of indices (self._front, self._back)
- modular arithmetic to advance and wrap

Task 2:
Implement the queue (correct, sid-effect free). No shifting of elements closer to the front of the queue
every time the next-in-line element is removed '''
class TwoDimensionalIQ:
    def __init__(self, n: int = 4):
        self._underlying: list[list[str]] = [[None for _ in range(n)] for _ in range(n)]
        self._n: int = n
        self._capacity: int = n * n
        self._usage: int = 0
        self._front_row: int = 0
        self._front_col: int = 0
        self._back_row: int = 0
        self._back_col: int = 0
    def get_usage(self) -> int:
        """
        Get the current usage of the queue (number of elements).
        """
        return self._usage

    def get_capacity(self) -> int:
        """
        Get the capacity of the queue (maximum number of elements).
        """
        return self._capacity

    def enqueue(self, value: str) -> bool:
        """
        Enqueue an element into the two-dimensional queue.
        """
        # Check if there is space in the queue and add the element if so.
        success: bool = self._usage < self._capacity #check if full
        #returns false if usage is at capacity
        if success: #if not full
            # Calculate the row and column to insert the new element based
            # on current usage.
            row = self._usage // self._n #see how much of row we have used (divided integer)
            col = self._usage % self._n #see how much column we have used (modulus - remainder)
            #calculates what is remaining, i should reverse this
            reversed_row = self._capacity - row - 1
            reversed_col = self._capacity - col - 1

            self._underlying[row][col] = value
            self._usage += 1
        #
        #return false is full
        return success

    def dequeue(self) -> str | None:
        """ Dequeue an element from the two-dimensional queue.
        """
        if self._usage == 0: #returns none if empty
            return None
        if self._usage > 0: #if we are not empty, dequeue
            #return the first element, using pointer, do not remove or shift
            result = self._underlying[self._front_row][self._front_col] #this is waiting room
            #removes at front (initialized at zero)
            #set cell to None and advance front with wrap
            self._underlying[self._front_row][self._front_col] = None
            #update our pointers
            self._front_row += 1
            self._front_col += 1
            if self._front_row == self._n: #if we are at the end of the row, wrap column
                self._front_col = 0 #reset to wrap
                self._front_row = 0
            self._usage -= 1 #decrease as we are removing from queue
        return result

    def list_queue(self) -> list[str]:
        """
        List all elements in the two-dimensional queue.
        """
        # Return a flat list of all elements in the queue.
        result = []
        # Iterate only up to current usage.
        for i in range(self._usage):
            # Calculate the row and column of the current element.
            row = i // self._n
            col = i % self._n
            # Append the element to the result list.
            result.append(self._underlying[row][col])
        return result

def visualize(item : str, count : int, success : bool, list : list[str]) -> list[str]:
    index = [1, 2, 3, 4]
    front_pointer = count
    back_pointer = len(list) - count - 1
    if success:
        list[count] = item
        print("waiting room = ", list)
        print("index = ", index)
        print("front pointer = ", front_pointer)
        print("back pointer = ", back_pointer)
        print("\n\n")
    return list

if __name__ == "__main__":
    test = TwoDimensionalIQ(2)
    items_to_add = ["Alice", "Bob", "Cathy", "Derek", "Eva"]
    list = ["", "", "", ""]
    count = 0
    for item in items_to_add:
        success = test.enqueue(item)
        if success:
            list = visualize(item, count, success, list)
            count += 1
        print(f"Enqueuing {item:<6}: {'Successful' if success else 'Failed'}")
    print(test.list_queue())
