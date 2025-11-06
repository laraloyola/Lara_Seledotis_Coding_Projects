'''
Lara Seledotis
COMP 271
MIDTERM October 7th 2025

clinic uses n x n waiting room in rows
new arrivals sit at first seat scanning front to back, left to right
next person called is front left seat

goal: stack only those who arrived last and who are next. use n x n grid as seating area
where the front of queue and back of queue pointer advance in row-major order (wrapping around)
'''
'''Class creates a queue matrix with row-major order and wrap around logic. 
Reads left to right like a book. Uses modular arithmatic (remainders)
to keep track of front and back pointers. More efficient logic
than the traditional waiting room because the people don't shift closer to front
but instead we keep track of first and last person in queue and make sure
to enqueue and dequeue with respect to them. Works as efficient FIFO. 
Load in the back (enqueue) and unload in the front (dequeue). '''
class TwoDimensionalQ:
    '''Initialize everything'''
    def __init__(self, n: int = 4):
        self._underlying: list[list[str]] = [[None for _ in range(n)] for _ in range(n)]
        self._n: int = n
        self._capacity: int = n * n
        self._usage: int = 0
        self._front_row: int = 0
        self._front_col: int = 0
        self._back_row: int = 0
        self._back_col: int = 0
    '''get our current usage value back. see how much of queue is full'''
    def get_usage(self) -> int:
        """ get usage. status of what is in the queue (how many spaces filled)"""
        return self._usage
    '''get the current capacity. maximum number of elements'''
    def get_capacity(self) -> int:
        """ get capacity. Maximum number of elements """
        return self._capacity
    ''' place things in the back. enter in the queue. '''
    def enqueue(self, value: str) -> bool:
        """ PLACE AT BACK """
        success: bool = self._usage < self._capacity #check if full, if so returns false
        if success: #if not full
            #add item to back row
            self._underlying[self._back_row][self._back_col] = value
            self._usage += 1 #increment usage
            #advance back queue
            self._back_col = (self._back_col + 1) % self._n
            #wrap around logic for next enqueue
            if self._back_col == 0: #check if we reached max column
                self._back_row = (self._back_row + 1) % self._n #increase our row
        return success
    '''unload the queue, FIFO - first in first out. unload from the front. 
    use the front pointers. '''
    def dequeue(self) -> str | None:
        """ REMOVE AT FRONT"""
        if self._usage > 0: #if we are not empty, dequeue
            #return the first element, using pointer, do not remove or shift
            result : str = self._underlying[self._front_row][self._front_col] #this is waiting room
            #removes at front (initialized at zero)
            #set cell to None and advance front with wrap
            self._underlying[self._front_row][self._front_col] = None
            #update our front pointers
            self._front_col = (self._front_col + 1) % self._n  # update column
            #checks if max column
            if self._front_col == 0: #RESET WRAP
                self._front_row = (self._front_row + 1) % self._n #increases row if max column
            self._usage -= 1 #decrease as we are removing from queue
        else: #USAGE == 0
            result = None #EMPTY LIST
        return result

    def list_queue(self) -> list[str]:
        """ List all elements in the two-dimensional queue."""
        # Return a flat list of all elements in the queue.
        result : list[str] = []
        row : int = self._front_row
        col : int = self._front_col
        # Iterate only up to current usage.
        for i in range(self._usage):
            # Calculate the row and column of the current element.
            # Append the element to the result list.
            result.append(self._underlying[row][col]) #append list value to add
            col = (col+1) % self._n #update column
            if col == 0: #wrap logic
                row = (row + 1) % self._n #increment our row on wrap
        return result
    def peek(self) -> str | None:
        """ Peek element from queue"""
        if self._usage > 0:
            #look at current output (front)
            #str type annotation because it uses specific string not all of it
            window : str = self._underlying[self._front_row][self._front_col]
        else: #USAGE == 0
            window : str = None #empty list
        return window
    def __bool__(self) -> bool:
        ''' returns true if queue is not empty. false if empty'''
        if self._usage == 0: #no usage, empty
            status : bool = False
        else:
            status : bool = True
        return status
    def __repr__(self) -> str:
        ''' string representation of queue'''
        #snapshot of object and key attributes
        window : list[list[str]] = self._underlying #show all of it, type annotation from __init__
        front_pointer : int = [self._front_row, self._front_col]
        back_pointer : int = [self._back_row, self._back_col]
        return (f"Our queue: {window} "
                f"\nUsage: {self._usage} "
                f"\nCapacity: {self._capacity} "
                f"\nFront pointer (r,c): {front_pointer} "
                f"\nBack pointer (r,c): {back_pointer}")

if __name__ == "__main__":
    test = TwoDimensionalQ(2)
    items_to_add = ["Alice", "Bob", "Cathy", "Derek", "Eva"]
    count = 0
    for item in items_to_add:
        success = test.enqueue(item)
        print(f"Enqueuing {item:<6}: {'Successful' if success else 'Failed'}")
        print(test.list_queue()) #show current queue
    print("Full queue", test.list_queue())
    print("Add to Full queue", test.enqueue("Lara"))
    print("Full queue status", test.list_queue())
    print("Dequeue1:", test.dequeue())
    print("usage", test.get_usage()) #should be 3
    print("Capacity:", test.get_capacity()) #should be 4
    print("post dequeue1", test.list_queue())
    print("Dequeue2:", test.dequeue())
    print("represent", test.__repr__())
    print("post dequeue2", test.list_queue()) #should wrap here
    print("peek into queue", test.peek())
    print("Dequeue3:", test.dequeue())
    print("post dequeue3", test.list_queue())
    print("Dequeue4:", test.dequeue())
    print("post dequeue4", test.list_queue())  # should be empty now
    print("represent", test.__repr__())
    print("remove from empty queue", test.dequeue())
    print("remove from empty queue status", test.list_queue())




