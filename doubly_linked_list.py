'''
Three problems in this assignment.
1. Middle of double linked list
2. loop is double linked list
3. detect a gap in double linked list
'''
#from email.feedparser import headerRE

''' '''
from node import Node

class DoublyLinkedList:

    def __init__(self):
        self.__head = None
        self.__tail = None
        self.__size = 0
        
    def get_head(self):
        return self.__head

    def get_tail(self):
        return self.__tail

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        nodes = []
        current = self.__head
        while current is not None:
            nodes.append(str(current))
            current = current.get_next()
        return " <-> ".join(nodes)

    def is_empty(self):
        return self.__size == 0

    def get_size(self):
        return self.__size

    def add_to_back(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.__head = new_node
        else:
            new_node.set_prev(self.__tail)
            self.__tail.set_next(new_node)
        self.__tail = new_node
        self.__size += 1

    def add_to_front(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.__tail = new_node
        else:
            new_node.set_next(self.__head)
            self.__head.set_prev(new_node)
        self.__head = new_node
        self.__size += 1
    def find_middle(self) -> None | Node: #TASK 1
        ''' function to find the middle node of a doubly linked list
        with pointers that move at the same speed. One node at a time.
        Method checks if empty and if not it moves left pointer towards
        right and the right pointer towards the left, when they equal that is the middle.
        middle index is returned'''
        if self.is_empty():
            return None
        #move from each end towards the center at same speed,
        #they will collide in the middle
        left_side = self.__head #initialize left as head
        right_side = self.__tail #initialize right as tail
        #while they have not collided and they are not about to collide
        while left_side != right_side and left_side.get_next() != right_side:
            #iterate each side towards the center
            left_side = left_side.get_next() #next is moving towards right as list index increase
            right_side = right_side.get_prev() #right gets lower index to move left
        #loop will end when they collide or are about to collide (even vs odd)
        return left_side #returns midpoint index

    def has_loop(self) -> bool:
        ''' function to tell if single linked list has a loop.
         method to detect a loop without traversing the link at all (no pointers)
        checks if the head or tail is in a loop. if loop then head has prev,
        if loop then tail has a next rather than ground. Only detects loop at ends not
        if there is loop in the middle (because we cannot traverse the list)'''
        loop = False
        if self.is_empty():
            return False #empty data has no loop, stops function
        #doubly linked list must have tail going to none and head going to none
        #if not, there is a circular loop within the list
        if self.__tail.has_next() or self.__head.has_prev(): #if either of these are 1 (should be zero for nonlooped)
            loop = True
        return loop

    def has_gap_forward(self) -> bool:
        ''' returns true if DoublyLinkedList object has gap in forward direction, else false
        gap in forwards direction would mean that node's next does
        not equal node+1 prev'''
        pointer = self.__head #start at head
        gap_exist = False
        while pointer and pointer.has_next():#make sure there is next pointer and pointer not empty
            pointer_next = pointer.get_next() #get the next value
            if pointer_next.get_prev() != pointer:
                gap_exist = True
            pointer = pointer_next #iterate while loop
        return gap_exist #if we went through entire loop and go gap found return false

    def has_gap_backward(self) -> bool:
        ''' returns true if DoublyLinkedList object has gap in backwards direction, else false.
         same as forward but reverse. nodes previous should equal nodes next'''
        pointer = self.__tail
        gap_exist = False #null value, turns true if we find one
        while pointer and pointer.has_prev(): #make sure there is prev and pointer not empty
            pointer_prev = pointer.get_prev() #get previous value
            if pointer_prev.get_next() != pointer: #if previous does not equal current / next, gap exists
                gap_exist = True
            pointer = pointer_prev #iterate pointer reverse (moving right to left)
        return gap_exist

    def has_gap_(self) -> bool:
        ''' method returns true if DoublyLinkedList object has gap in either forward
        or backwards direction and false otherwise.
         It calls both functions to check if there is a forward or
         backwards gap, if either exists it returns true'''
        #return gap status
        return self.has_gap_forward() or self.has_gap_backward()



def main():
    dll_odd = DoublyLinkedList()
    #create list
    for i in range(1, 10): #[1,2,3,4,5,6,7,8,9]
        dll_odd.add_to_back(i)
    print("og list", dll_odd.__str__())
    middle_odd = dll_odd.find_middle()
    print("Middle index", middle_odd) #for odd
    dll_even = DoublyLinkedList() #reset initial status by calling this again
    for i in range(1, 9): #[1,2,3,4,5,6,7,8]
        dll_even.add_to_back(i)
    print("og list", dll_even.__str__())
    middle_even = dll_even.find_middle()
    print("Middle index", middle_even) #for even

    #checking for loop
    #making the loop by setting head to tail
    looped_list = DoublyLinkedList()
    for i in range(1,9):
        looped_list.add_to_back(i)
    #get head and tail
    head = looped_list.get_head()
    tail = looped_list.get_tail() 
    #set head and tail to point to eachother
    tail.set_next(head)
    head.set_prev(tail)
    print("loop status", looped_list.has_loop()) #should be true
    
    #checking for gap
    #make gap list
    gapped_list = DoublyLinkedList()
    for i in range(1,5):
        gapped_list.add_to_back(i)
    node1 = gapped_list.get_head().get_next() #call head value and get what comes after
    node2 = node1.get_next()
    node1.set_next(node2.get_next()) #change heads node to point after node 2 rather than node 2 (gap)
    print("gapped list", gapped_list)
    print("gap status overall", gapped_list.has_gap_())
    print("gap status overall", gapped_list.has_gap_forward())
    print("gap status overall", gapped_list.has_gap_backward())

    #test w upgapped
    ungapped = DoublyLinkedList()
    for i in range(1, 9):
        ungapped.add_to_back(i)
    print("ungapped list", ungapped)
    print("gap status (should be false)", ungapped.has_gap_())

    #check all functions with empty list
    empty_list = DoublyLinkedList()
    print(empty_list.find_middle())
    print(empty_list.has_loop())
    print(empty_list.has_gap_forward())
    print(empty_list.has_gap_backward())
    print(empty_list.has_gap_())

main()















