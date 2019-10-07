# CS 111 Problem Set 4
# Caesar Cipher Skeleton
#

import string
import random

WORDLIST_FILENAME = "words.txt"
# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    return wordlist

wordlist = load_words()

def is_word(wordlist, word):
    """
    Determines if word is a valid word.
    wordlist: list of words in the dictionary.
    word: a possible word.
    returns True if word is in wordlist.
    Example:
    >>> is_word(wordlist, 'bat') returns
    True
    >>> is_word(wordlist, 'asdf') returns
    False
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in wordlist

def random_word(wordlist):
    """
    Returns a random word.
    wordlist: list of words  
    returns: a word from wordlist at random
    """
    return random.choice(wordlist)

def random_string(wordlist, n):
    """
    Returns a string containing n random words from wordlist
    wordlist: list of words
    returns: a string of random words separated by spaces.
    """
    return " ".join([random_word(wordlist) for _ in range(n)])

def random_scrambled(wordlist, n):
    """
    Generates a test string by generating an n-word random string
    and encrypting it with a sequence of random shifts.
    wordlist: list of words
    n: number of random words to generate and scamble
    returns: a scrambled string of n random words
    NOTE:
    This function will ONLY work once you have completed your
    implementation of apply_shifts!
    """
    s = random_string(wordlist, n) + " "
    shifts = [(i, random.randint(0, 26)) for i in range(len(s)) if s[i-1] == ' ']
    return apply_shifts(s, shifts)[:-1]

def get_fable_string():
    """
    Returns a fable in encrypted text.
    """
    f = open("fable.txt", "r")
    fable = str(f.read())
    f.close()
    return fable


# (end of helper code)
# -----------------------------------

#
# Problem 1: Encryption
#
def build_coder(shift):
    alphabet = list(string.ascii_lowercase + ' ' + string.ascii_lowercase + ' ')
    upper_alphabet = list(string.ascii_uppercase + ' ' + string.ascii_uppercase + ' ')
    test_dict = {}

    for i in range(len(alphabet)):
        test_dict[alphabet[i]] = alphabet[shift + i]
        test_dict[upper_alphabet[i]] = upper_alphabet[shift + i]

        if upper_alphabet[i] == ' ':
            test_dict[' '] = upper_alphabet[shift + i].lower()

        if alphabet[i] == ' ' or upper_alphabet[i] == ' ':
            break

    return test_dict


def build_encoder(shift):
    return build_coder(shift)


def build_decoder(shift):
    return build_coder(-shift)


def apply_coder(text, coder):
    """
    TODO:
        1. Make empty String
        2. for letter in 'text': if each element of letter belongs in 'text': add it onto empty string 
    """ 

    user_text = ''
    for element in text:
        if element in string.ascii_lowercase or element == ' ' or element in string.ascii_uppercase:
            user_text += coder[element]
        else:
            user_text += element # normal letter

    return user_text


def apply_shift(text, shift):
    return apply_coder(text, build_encoder(shift))


#
# Problem 2: Codebreaking.
#
def find_best_shift(wordlist, text):
    """
    TODO:
    Basically like finding biggest word. 
    1. find out if word in test_list
    2. is steps > most_words then set most_words = steps and the answer to the current shift
    """

    most_words = 0
    answer = 0
    for shift in range(1, 27):
        steps = 0
        test_list = apply_coder(text, build_decoder(shift)).split() # breaks up word into each element in list
        for word in test_list:
            if is_word(wordlist, word):
                steps += 1
        if steps > most_words:
            most_words = steps
            answer = shift
    return answer

   
#
# Problem 3: Multi-level encryption.
#
def apply_shifts(text, shifts):
    """
    TODO:
    GOAL - Use recursion 
    0. (-->0,0) = [:stop:]
    1. (0,0<--) = Shift
    2. set a variable to always equal (-->0,0) or [0][0]
    3. Set a variable to always equal (0,0<--) or [0][1]

    """
    copy_text = text

    for i in shifts:
        Stop = copy_text[:i[0]]
        shifting_by = copy_text[i[0]:]
        copy_text = Stop + apply_shift(shifting_by, i[1])
        
    return copy_text

 
#
# Problem 4: Multi-level decryption.
#
def find_best_shifts(wordlist, text):
    global shifts_list #create a global list called shifts_list. This will store the valid shifts found across recursive calls
    shifts_list = []
    for shift in range(28): #goes through all possible shifts from 1 to 27
##        print
##        print "Current shift: " , shift
        s = apply_shift(text, shift) #applies the shift to the text (from 0)
##        print "shifted text(s): %s" % s
        try: #look to see if the shifted text contains a space (indicates a possible word)
            space = s.index(' ') #see above
##            print "Space = " , space
##            print
            if is_word(wordlist, s[:space]): #Checks if the text from start of string to the space found is a word
##                print "Valid word found from position 0 with shift %d" % shift
                find_best_shifts_rec(wordlist, s, space+1) #calls the recursive function (below), starting at the position just beyond the space (and therefore after the valid word that was found)
##                print "(OG)Shifts_list just before checking for none:" , shifts_list
                if None in shifts_list: #Check for none in shifts_list - None indicates that the current shift lead to a dead end somewhere down the line of shifts/decryption
##                    print "None in shifts_list - clearing shifts_list"
                    shifts_list = [] #resets shifts_list
##                    print "About to pass"
##                    print
                    pass #passes to next shift in iteration
                else: #If none is not found in shifts_list, that is good - means the shifts ended up correctly finding the end of a string/sentence and that string/sentence has all valid words
##                    print "None not found in shifts list"
                    shifts_list.append((0,shift)) #Appends the first shift (the original that led to correct series of shifts) to shifts_list
##                    print "Shifts list currently: %s" % shifts_list
                    shifts_list = shifts_list[::-1] #Shifts have been being added backwards - the last correct shift is added first, and each shift after that is added up the levels of recursion. The result is a valid shifts_list, but in reverse. This simply switches the order
##                    print "flipped:" , shifts_list
                    break #breaks out of loop, so that the function can return the correct shifts_list (did this mainly so that the function only has one return line)                 
        except ValueError: #If initial shift does not find a space, the string/sentence may only have one word, this checks to see if thats the case
##            print "value error - substring not found"
            if is_word(wordlist, s): #if the string/sentence with no space is indeed a valid word, that means it really is only one word long
##                print "End of sentence found"
                shifts_list.append((0, shift)) #appends this shift to the shifts_list
                break #breaks out of the loop so that the function can return
            else: #if the string that has no space is not actually a word, the loop just continues at the next iteration. This 'else' is only here to guide bug checking - it leads to the print statement below.
##                print "No space and no words"
                pass #Unnecessary, but put here to easier follow flow, and also to be able to only have to comment out the prints, and not this else statement as well (if you don't, it brings up a syntax error because there is an else statement but the next line of code is not indented under it)
##    print "Total process about to return: " , shifts_list
##    print shifts_list
    return shifts_list #returns the valid shifts_list. Done! 


def find_best_shifts_rec(wordlist, text, start):
    global shifts_list
    passed_shifts_list = shifts_list[:]
    s_pre = text[:start]
    s_post = text[start:] 
    for shift in range(28): #goes through all possible shifts
        s = s_pre + apply_shifts(s_post, [(0, shift)]) #applies current shift to the second segment of the string, the one that is still encrypted
##        print "Starting at: " , start
##        print "current shift is: " , shift
##        print "shifted text(s): %s" % s
        try: #checks to see if there are any spaces created with the current shift
            space = s.index(' ', start) #see above
##            print "Space = " , space
##            print
            if is_word(wordlist, s[start:space]):#checks to see if the word from the start parameter to the space that was found is a valid word
##                print "Recursive function will return: (%s,%s)" % (start, shift)
##                print "Recursive function about to pass text with start = %d + 1" %space
                #may want to append here. passed_shifts_list will still be what it was when it passed in, but the next level will have these shifts in it
                find_best_shifts_rec(wordlist, s, space+1) #Recursively calls this function with a new start parameter, which is one position past where the space (indicating the end of a valid word) was found
                if None in shifts_list: #When recursive calls have finished, check for None in shifts_list (None indicates that a recursive call came to a dead end)
##                    print "None in shifts_list:", shifts_list
##                    print "Resetting shifts_list to what it was at this level of recursion:" , passed_shifts_list
                    shifts_list = passed_shifts_list[:] #resets shifts_list to what it was at this level of recursion, so that the function can continue checking possible shifts. THIS WAS A BIG BUG - ALIASING. HAVE shifts_list = copy of passed_shifts_list, other wise things get messed up!!!
##                    print "Shifts_list now equals:" , shifts_list
##                    print "About to pass"
##                    print
                    pass #passes to next shift in the iteration
                else:
##                    print "None not found in shifts_list:" , shifts_list
                    shifts_list.append((start,shift)) #Since None was not found in shifts list, the current (start,shift) is a good shift and is appended to shifts_list (as a tuple)
                    return #Ends this level of recursion
        except ValueError: #Prevent a ValueError from stopping the program. This occurs when no space is found in the s.index(). This either indicates a bad shift, or ideally, the end of a string/sentence
##            print "value error - substring not found"
            if is_word(wordlist, s[start:]): #Checks to see if the word found from start to the end of the string/sentence is a valid word (which indicates the end of a sentence)
##                print "End of sentence found"
##                print
##                print "Recursive function about to return: (%s,%s)" % (start,shift)
##                print
                shifts_list.append((start,shift)) #Since the word was valid, the (start,shift) is appended to shifts_list
                return #Ends this level of recursion
            
##    print "Recursive loop has completed with no words found"
##    print
    shifts_list.append(None) #Since no valid shift was found, None is appended to shifts_list so that the next level up knows to continue looking
    return #End this level of recursion


def decrypt_fable():
    """
    Using the methods you created in this problem set,
    decrypt the fable given by the function get_fable_string().
    Once you decrypt the message, be sure to include the fable
    as a comment at the end of this problem set.
    returns: string - fable in plain text
    """
    ### TODO.
    fable = str(get_fable_string())
    shifts = find_best_shifts(wordlist, fable)
    print(apply_shifts(fable, shifts))

decrypt_fable()
# What is the fable?
"""
An Ingenious Man who had built a flying machine invited a great concourse of people to see it go up.
at the appointed moment, everything being ready, he boarded the car and turned on the power. the machine 
immediately broke through the massive substructure upon which it was builded, and sank out of sight into the earth, 
the aeronaut springing out a rely in time to save himself. "well," said he, "i have done enough to demonstrate the 
correctness of my details. the defects," he added, with a add hat the ruined brick work, "are merely a sic and fundamental." 
upon this assurance the people came ox ward with subscriptions to build a second machine
"""