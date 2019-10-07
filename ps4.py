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
    global shifts_list
    shifts_list = []
    for shift in range(28):
        s = apply_shift(text, shift)
        try:
            space = s.index(' ')
            if is_word(wordlist, s[:space]):
                find_best_shifts_rec(wordlist, s, space+1)
                if None in shifts_list:
                    shifts_list = []
                    pass 
                else: 
                    shifts_list.append((0,shift)) 
                    shifts_list = shifts_list[::-1]
                    break 
        except ValueError:
            if is_word(wordlist, s):
                shifts_list.append((0, shift))
                break

    return shifts_list


def find_best_shifts_rec(wordlist, text, start):
    global shifts_list
    passed_shifts_list = shifts_list[:]
    s_pre = text[:start]
    s_post = text[start:] 
    for shift in range(28):
        s = s_pre + apply_shifts(s_post, [(0, shift)])
        try:
            space = s.index(' ', start)
            if is_word(wordlist, s[start:space]):
                find_best_shifts_rec(wordlist, s, space+1)
                if None in shifts_list:
                    shifts_list = passed_shifts_list[:] 
                    pass
                else:
                    shifts_list.append((start,shift))
                    return 
        except ValueError:
            if is_word(wordlist, s[start:]):
                shifts_list.append((start,shift)) 
                return
            
    shifts_list.append(None) 
    return 


def decrypt_fable():
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