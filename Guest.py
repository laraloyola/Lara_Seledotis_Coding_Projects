# UPDATED __str__: Oct 15
class Guest:

    """Class representing guests for our Hotel Alphabetical. These objects
    are essentially nodes in a linked list. Each hotel room is effectively a
    linked list of guests, placed in that room based on some hashing function.
    """

    def __init__(self, name: str):
        self.name = name
        self.next = None  # Pointer to the next guest in the linked list

    def __repr__(self):
        return f"Guest({self.name})"

    def set_next(self, next_guest):
        self.next = next_guest

    def get_next(self):
        return self.next

    def has_next(self):
        return self.next is not None

    def get_name(self):
        return self.name

    def __str__(self):
        return self.name   # UPDATED Oct 15
