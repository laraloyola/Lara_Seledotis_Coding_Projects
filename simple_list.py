#reverse a list of string to a string
#measure the similarity of two lists
#report the similarity of two lists using format specifier
#coutn symbol frequencies using a list instead of a dictionary
import sys # to check memory usage
'''  returns a string with contents of data list in reverse order
    one element per line
    each element progressively tabbed by as many spaces asa to the right as specified by parameter tab_by
    if list is empty or null, method should return 'None'
    no negative indices
    stack them in a stack, then remove from stack to reverse 
    
    My method: it starts off by having a large indent, then it checks
    if there is anything in data, if not returns None (which
    is why we do the pipeline -> str | None)
    and then it loops through each word in the list
    if it is the first word (not string - as string is the previous value)
     it prints the word and zero indent. if it is the non-first word
     it adds a new line, the indent, and the word (if string section)
     it decreases the tab length each time as the loop goes through from zero
     to max and then the final value string updates from max downto 0 with 
     decreasing tabs'''
def reverse_list_string(data: list[str], tab_by: int) -> str | None:
    if not data:
        return None
    indent = len(data) * tab_by  #start high and then move down
    string = "" #null string
    for word in data:
        line_break = (" " * indent) + word
        if string:
            string = line_break + ("\n" + string)
        else:
            string = line_break + ""
        #string = line_break + ("\n" + string if string else "") #increase our indent
        indent -= tab_by #increase tab length on each word
    return string
''' this takes in the strings and loops through to see if any value in our
reference matches anything in target. for each word in target
it will loop through all of reference and see if it works. if it 
exists we will increase exists_in_red and this will add to our count. At
the end it will print the float value'''
def measure_similarity(target: list[str], reference: list[str]) -> float:
    #returns value s between 0 and 1
    exists_in_ref = 0
    for i in (range(len(target))):
        for j in range(len(reference)):
            if target[i] == reference[j]: #loop through reference and see if target is inside
                exists_in_ref += 1
    s = exists_in_ref / len(target)
    return s
''' report similarity will call the function measure similarity to get the 
float value but then will print this in string form as a percentage'''
def report_similarity(target: list[str], reference: list[str]) -> str:
    s = measure_similarity(target, reference)
    return f"{(s*100):.2f}%"
''' method from sakai on frequency counting '''
def simple_frequency_counter(message: str) -> dict[str, int]:
    #for testing / comparison
    frequency = {} #tuple
    if message is not None and len(message) > 0:
        for char in message:
            if char in frequency:
                frequency[char] += 1
            else:
                frequency[char] = 1
    return frequency
''' frequency counter which loops through the message and each character. 
it ignores the spaces (counting them separately). If a character is not
a space it will use the ord() function - shown in section 4.3.2 of pearson -
and will sort the characters alphabetically using ASCII code
 ord(char) - ord('a') (we add one to account for the space)
then it will increase the index. It returns a list of integers that calls
the freuqnecy of each chracter (frequency[0] gives 6 spaces and 
frequency[1] gives 2 'a' characters etc'''
def efficient_frequency_counter(message: str) -> list[int]:
    #count character frequencies
    frequency = [0] * 27 #for each letter in alphabet plus space
    if message:
        for char in message:
            if char == " ": #count empty spaces
                frequency[0] += 1
            else: #not empty space
                index = ord(char) - ord('a') + 1 #do the alphabet
                if 1 <= index <= 26:
                    frequency[index] += 1
    return frequency

''' testing the  code'''
def main():
    data = ["Howard", "Jarvis", "Morse", "Loyola", "Granville"]
    tab_by = 5
    print(reverse_list_string(data, tab_by))
    print("\n\n\n") 
    target = ["a", "b", "c", "d"]
    reference = ["c", "d", "e", "f"]
    similarity = measure_similarity(target, reference)
    print("Similarity", similarity)
    percentage = report_similarity(target, reference)
    print("Similarity percentage", percentage)

    pangram = "sphinx of black quarts judge my vow"
    frequency = simple_frequency_counter(pangram)
    print("Frequency", frequency)

    dict_freq = simple_frequency_counter(pangram)
    list_freq = efficient_frequency_counter(pangram)
    print("list_freq", list_freq)
    print(sys.getsizeof(dict_freq), "bytes for dict")
    print(sys.getsizeof(list_freq), "bytes for list")

main()
