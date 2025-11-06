# UPDATED: Oct 16 Added self._size = 0 in `_rehash`
from Guest import Guest    # UPDATED: Oct 15

class HotelAlphabetical:
    """Class representing a hotel where guests are stored in rooms based on
    the first initial of their names. Each room is a linked list of guests.
    """

    _DEFAULT_CAPACITY = 26
    _ASCII_LEFT_EDGE = ord("A")
    _ASCII_RIGHT_EDGE = ord("Z")
    _EMPTY = "boohoo, your hotel is empty."
    _NEXT_GUEST = " --> "

    _LOAD_FACTOR_THRESHOLD = 0.7
    _INCREMENT_FACTOR = 2

    def __init__(self, capacity: int = _DEFAULT_CAPACITY):
        self._capacity = capacity
        self._hotel = [None] * capacity  # Array of linked lists for each letter
        self._usage = 0  # number of array slots used
        self._size = 0

    def _get_index(self, name: str) -> int:
        """Compute the index in the hotel array based on the first
        initial of the guest's name."""
        # Default to 0 if name is None or empty or not A-Z
        room_index = 0
        if name is not None and len(name) > 0:
            # DISCUSSION POINT: should we be computing the first initial
            # here or should it be done in object Guest?
            initial_ascii = ord(name.upper()[0])
            if self._ASCII_LEFT_EDGE <= initial_ascii <= self._ASCII_RIGHT_EDGE:
                room_index = initial_ascii % self._capacity
        return room_index

    def _check_load_factor(self) -> bool:
        """Check if the load factor exceeds the threshold."""
        load_factor = self._usage / self._capacity
        return load_factor > self._LOAD_FACTOR_THRESHOLD

    def _rehash(self) -> None:
        """Rehash the hotel by increasing its capacity and reassigning guests."""
        # Preserve the old hotel array and its capacity
        old_hotel = self._hotel
        old_capacity = self._capacity
        # Create a new hotel array with increased capacity
        self._capacity *= self._INCREMENT_FACTOR
        # Initialize the new hotel array and reset usage
        self._hotel = [None] * self._capacity
        self._usage = 0
        self._size = 0       # UPDATE Oct 16
        # Reinsert all guests into the new hotel array
        for room in range(old_capacity):
            guest_in_room = old_hotel[room]
            while guest_in_room is not None:
                self.add_guest(guest_in_room.get_name())
                guest_in_room = guest_in_room.get_next()

    def add_guest(self, name: str) -> None:
        """Add a guest to the hotel."""
        if self._check_load_factor():
            self._rehash()
        # Compute the room index based on the first initial of the name
        room = self._get_index(name)
        # Create a new guest object
        guest = Guest(name)
        # Insert the guest at the front of the linked list for that room
        if self._hotel[room] is None:
            self._hotel[room] = guest
            self._usage += 1
        else:
            guest.set_next(self._hotel[room])
            self._hotel[room] = guest
        # Increment the current occupancy of the hotel
        self._size += 1

    def __repr__(self) -> str:
        hotel_string = self._EMPTY
        if self._size > 0:
            hotel_string = f"\nThere are {self._size} guest(s) in your hotel."
            hotel_string += f"\nThe hotel has a capacity of {self._capacity} rooms."
            hotel_string += f" and is using {self._usage} room(s)."
            hotel_string += f"\nThe load factor is {self._usage/self._capacity:.2f}."
            hotel_string += f" The {self._size} guest(s) are:"
            for room in range(self._capacity):
                if self._hotel[room] is not None:
                    hotel_string += f"\n\tRoom {room:02d}: "
                    guest_in_room = self._hotel[room]
                    while guest_in_room is not None:
                        hotel_string += f"{guest_in_room.get_name()}{self._NEXT_GUEST}"
                        guest_in_room = guest_in_room.get_next()
                    hotel_string += ""
        return hotel_string

    def exists(self, guest_name:str) -> bool:
        '''returns true if specified guest is present, false otherwise.
            takes in argument of string guestname to search for. returns the
            boolean present to state if guest is in hotel or not. searches
            through the hotel hash table (all the rooms) using the same logic as
            the __repr__ method to look through who is there. searching through
            current hotel and checks each room for guest_name'''
        present = False #null
        if self._size > 0:
            for room in range(self._capacity): #go through table and search for name
                guest_in_room = self._hotel[room] #checking the room for the name
                while guest_in_room is not None: #making sure guest is not none
                    if guest_in_room.get_name() == guest_name: #comparing the two strings
                        present = True #if they match then guest is in that room, return true
                    guest_in_room = guest_in_room.get_next() #get the next person down the list / keep moving
        return present

    def remove(self, guest_name: str) -> Guest | None:
        '''removes a guest if they are present from hotel. Returns guest if
        successful else method returns none. loops through the list if
        is it not none and determines if it matches. if it does it removes them
        and adjusts list links (connecting broken nodes). then it moves
        forward in the list. if the person to be removed is found and removed
        the loop stops'''
        # initialize None if guest is not found
        removed = None
        previous_guest = None  # gets previous Node
        room = self._get_index(guest_name)  # find where the guest is
        guest_in_room = self._hotel[room]  # get name of person in that room (should match guest_name)
        found = False

        while guest_in_room is not None and found == False:  # looping through the list
            if guest_in_room.get_name() == guest_name:  # check if the guest is in the hotel
                if previous_guest is None:  # used for if the guest is the only one in that room
                    self._hotel[room] = guest_in_room.get_next()  # from Guest function, get next node
                    if self._hotel[room] is None:  # if the hotel now empty reduce space used
                        self._usage -= 1
                else:  # if there are more than one person in room
                    previous_guest.set_next(guest_in_room.get_next())  # skip over the removed person and relink
                self._size -= 1  # adjust size
                removed = guest_in_room  # return who was removed
                guest_in_room.set_next(None)  # detach node
                found = True
            else:
                # next iteration moving forward if not found
                previous_guest = guest_in_room
                guest_in_room = guest_in_room.get_next()
        return removed




def main():
    hotel = HotelAlphabetical()
    print("\ninitial status")
    print(hotel.__repr__())
    # boundary conditions
    # remove empty hash
    print(hotel.exists("Lara"))  # expected False
    # check if name exists in empty hash
    print(hotel.remove("Dexter"))  # expected None

    hotel.add_guest("Nemo")
    print("added Nemo status")
    print(hotel.__repr__())

    guest_list = ["Weeknd", "Arianna Grande", "Kim K", "J Cole", "Kendrick", "Kanye", "Dory"]
    for celeb in guest_list: #adding people to our hotel from the list
        hotel.add_guest(celeb)
    print(hotel.__repr__())
    print("Is Nemo there?", hotel.exists("Nemo"))  # should be true
    print("Is Merlin there?", hotel.exists("Merlin"))  # should be false

    print("remove Dory")
    print(hotel.remove("Dory"))
    print("new hotel", hotel.__repr__())
    print("remove kim k", hotel.remove("Kim K"))
    print(hotel.__repr__())

main()
