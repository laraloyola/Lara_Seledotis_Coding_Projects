''' hotel with N rooms
step1) create N guest names
step2) assign them to rooms using hashcode
step3) measure how many collisions we detect
step4) run code multiple times, and compute average number of collisions'''

import random


class SimulateCollisions:

    # Constants for random string generation
    DEFAULT_MIN_LENGTH = 10
    DEFAULT_MAX_LENGTH = 15
    ASCII_OFFSET = ord("A")
    ASCII_SIZE = 26

    # Default hotel size
    DEFAULT_N = 1_024
    DEFAULT_GUESTS = DEFAULT_N

    # Default simulations
    DEFAULT_TRIALS = 10

    def __init__(self, N: int = DEFAULT_N, guests: int = DEFAULT_GUESTS, trials: int = DEFAULT_TRIALS, part : int = 1) -> None:
        ''' initialize our elements '''
        self.N = N #number of rooms
        self.guests = guests #number of guests
        self.trials = trials #number of trials
        self.part = part #for running the parts
        self.hotel = [None] * self.N
        #maybe add room index?

    def reset(self) -> None:
        """Reset the hotel for a new simulation."""
        self.hotel = [None] * self.N #resets to empty hotel

    def generate_random_string(self) -> str:
        """Generate a random string of length between min_length and max_length."""
        str_len = random.randint(self.DEFAULT_MIN_LENGTH, self.DEFAULT_MAX_LENGTH)
        abc = "abcdefghijklmnopqrstuvwxyz"
        random_string = ""
        for i in range(str_len):
            random_string += abc[random.randint(0, len(abc) - 1)]
        return random_string

    def hashcode(self, name: str) -> int:
        """A simple hash function for strings."""
        if self.part == 1:
            code = 0
            # original sum-based hashcode
            for char in name: #sum of the name characters
                code += ord(char)
        elif self.part == 2:
            #part 2 function
            code = 1 #initialize to 1 because we are multiplying
            for char in name:
                code *= ord(char)
                code %= 2**32 #overflow boundary, remainder of 32 bit hash memory
        elif self.part == 3:
            #part 3 function
            code = 0
            for i in range(len(name)):
                code += (ord(name[i]) * (31**(len(name) - 1 - i)))
        else: #default part 1
            code = 0
            # original sum-based hashcode
            for char in name: #sum of the name characters
                code += ord(char)
        return code

    def hash_function(self, name: str) -> int:
        """Hash function to map a name to a hotel room."""
        return self.hashcode(name) % self.N

    def guest_list(self, guests: int) -> list:
        '''create a guest list with random strings generated'''
        roster = []
        for i in range(guests): #create a list of names of size N
            name = self.generate_random_string()
            roster.append(name)
        return roster

    def gen_collisions(self) -> int:
        '''function checks the names on the guest list and looks for them
        in the hotel. if they are already in the hotel it records that as a
        collision and returns the total number of collisions after going through
        all the guest list. '''
        # simulate once
        self.reset()
        collisions = 0
        for name in (self.guest_list(self.guests)):
            # going through each name and checking
            room = self.hash_function(name) #getting function assigned to name
            if self.hotel[room] is not None:  # room already full
                collisions += 1  # room booked
            else:
                self.hotel[room] = name #if not booked at name in
        return collisions #return how many collisions

    def main(self):
        """Run multiple simulations and report average collision rate."""
        total_col = 0
        self.trials = 100 #increase our trial number
        for trial in range(self.trials): #loop through # trials
            total_col += self.gen_collisions()
        average = total_col / self.trials
        rate = (average / self.guests) * 100
        print("guests", self.guests)
        print("trials", self.trials)
        print("average collisions", average)
        print(f"Collision rate {rate:.2f}%")







def main1():
    ''' run simulations to get '''
    #run all parts
    for i in range(1, 4): #run the three parts
        experiment = SimulateCollisions(part = i)
        print("\n Running Part", i)
        experiment.main()



main1()

''' ANALYSIS

We observe that the collision rate is the lowest in part 3 and the highest in part 2.
This means that the best hashcode algorithm is the summation of
ord(name[i] multiplied by 32 to the power of string_length minus 1 - i.
This hashcode produces the most spread out results resulting in minimal collisions.  

Part 1 is a simple approach but does have some collisions due to there
not being a lot of variability in sum. When values are clumped together this is
disadvantageous but it's not bad if there are clusters of empty space.
This is the average case. 

Part two is the worst case as the multiplication causes large numbers which cluster together.
It adds the hotel rooms next to each other which creates bad clusters. 

Part 3 is the best case scenario with the lowest collision rate.
I believe this is because the 31 to the power of the name length - 1 - i
is helpful for creating separation thus avoiding collisions.
Seems to spread the rooms out a bit more evenly across the hotel. '''



