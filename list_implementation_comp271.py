# Starter code for MyList

from typing import Any
class MyList: #create class

    _EMPTY = "List is empty"
    _RESIZE_BY = 2

    def __init__(self, maximum_size: int = 4):
        """Create an empty list with a fixed size block specified by parameter
        maximum_size. The object tracks how many actual elements are in the list
        using the attribute __actual_size.
        """
        self._maximum_size: int = maximum_size
        self.__actual_size: int = 0
        self._data: list = [None] * self._maximum_size

    def __len__(self) -> int:
        return self.__actual_size #return integer actual size

    def __str__(self) -> str:
        return f"{self._data[:self.__actual_size]}" #return string representation of list, only get the meaningful portion

    def _change_size(self): #private
        new_size = self._maximum_size * self._RESIZE_BY
        new_data = [None] * new_size #create larger memory size
        for i in range(self.__actual_size):  # moving old list into new memory
            new_data[i] = self._data[i]  # move list over
        self._data = new_data  # make sure list is consitent
        self._maximum_size = new_size  # change our max to new max

    def append(self, value) -> None:
        if self.__actual_size == self._maximum_size: #if less than max we can add more
            self._change_size() #we hit the max and need to change size, call _change_size functions
        self._data[self.__actual_size] = value #appending
        self.__actual_size += 1  # change our size


    def insert(self, index: int, value) -> None:
        if self.__actual_size == self._maximum_size: #checking
            self._change_size()
        if index < 0 or index > self.__actual_size: #checking our range
            print("Index out of range")
        else:
            for i in range(self.__actual_size, index, -1): #go from max, down to index, left to right key
                self._data[i] = self._data[i - 1] #moving to the right, higher index gets value of lower index
        #outside of loop so they are always done
            self._data[index] = value #inserting our value
            self.__actual_size += 1 #changing our size post insertion


    def remove(self, index: int) -> Any:
        if index >= self.__actual_size or index < 0: #out of range
            print("Index out of range")
            remove_val = None
        else:
            remove_val = self._data[index]
            for i in range(index, self.__actual_size - 1): #moving through right half of list
                self._data[i] = self._data[i+1] #shifting to the left
            self._data[self.__actual_size - 1] = None #replace with empty string
            self.__actual_size -= 1 #update our size
        return remove_val


    def pop(self) -> Any:
        if self.__actual_size == 0:
            print("Cannot pop from empty list")
            pop_val = None
        else:
            pop_val = self._data[self.__actual_size - 1] #store last in list to temp
            self._data[self.__actual_size - 1] = None #remove it, (replace with none)
            self.__actual_size -= 1 #change our size
        return pop_val
# --- Simple testing ---
if __name__ == "__main__":
    my_list = MyList()
    # Write tests using this object to verify your methods work correctly.
    #call each function
    print("original length", my_list.__len__())
    print("original list", my_list)
    for i in range (10): # add some values
        my_list.append(i)
    print("added values to list", my_list.__str__())
    print("checking", my_list)
    print("\nnew length", my_list.__len__())

    my_list.insert(0, 23)
    print("\ninsert value at start", my_list.__str__())
    print("new length", my_list.__len__())
    print("checking", my_list)

    my_list.remove(0) #removing start value
    print("\nremoved list", my_list.__str__())
    print("checking", my_list)

    remove_val = my_list.remove(2)  # removing middle value
    print("\nremoved list", my_list.__str__())
    print("removed value", remove_val)
    print("checking", my_list)

    pop_val = my_list.pop()
    print("\npopped list", my_list.__str__())
    print("popped value", pop_val)
    print("checking", my_list)

######## repeat with strings
    # call each function
    #clear the list
    for i in range(len(my_list)):
        #pop until it is empty
        my_list.pop()
    print("\n\n\nNEW LIST original length", my_list.__len__())
    print("original list", my_list)
    fruits = ["Apples", "bananas", "oranges", "blueberries", "cherries"]
    for i in range(len(fruits)):  # add some values
        my_list.append(fruits[i])
    print("added values to list", my_list.__str__())
    print("checking", my_list)
    print("\nnew length", my_list.__len__())

    my_list.insert(0, "Peaches")
    print("\ninsert value at start", my_list.__str__())
    print("new length", my_list.__len__())
    print("checking", my_list)

    my_list.remove(0)  # removing start value
    print("\nremoved list", my_list.__str__())
    print("checking", my_list)

    remove_val = my_list.remove(2)  # removing middle value
    print("\nremoved list", my_list.__str__())
    print("removed value", remove_val)
    print("checking", my_list)

    pop_val = my_list.pop()
    print("\npopped list", my_list.__str__())
    print("popped value", pop_val)
    print("checking", my_list)
