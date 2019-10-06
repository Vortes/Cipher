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
    Applies a sequence of shifts to an input text.
    text: A string to apply the Ceasar shifts to 
    shifts: A list of tuples containing the location each shift should
    begin and the shift offset. Each tuple is of the form (location,
    shift) The shifts are layered: each one is applied from its
    starting position all the way through the end of the string.  
    returns: text after applying the shifts to the appropriate
    positions
    Example:
    >>> apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    """
    ### TODO.
 
#
# Problem 4: Multi-level decryption.
#
def find_best_shifts(wordlist, text):
    """
    Given a scrambled string, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.
    Hint: Make use of the recursive function
    find_best_shifts_rec(wordlist, text, start)
    wordlist: list of words
    text: scambled text to try to find the words for
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    
    Examples:
    >>> s = random_scrambled(wordlist, 3)
    >>> s
    'eqorqukvqtbmultiform wyy ion'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> shifts
    [(0, 25), (11, 2), (21, 5)]
    >>> apply_shifts(s, shifts)
    'compositor multiform accents'
    >>> s = apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    >>> s
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> print(apply_shifts(s, shifts))
    Do Androids Dream of Electric Sheep?
    """

def find_best_shifts_rec(wordlist, text, start):
    """
    Given a scrambled string and a starting position from which
    to decode, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.
    Hint: You will find this function much easier to implement
    if you use recursion.
    wordlist: list of words
    text: scambled text to try to find the words for
    start: where to start looking at shifts
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    """
    ### TODO.

def decrypt_fable():
    """
    Using the methods you created in this problem set,
    decrypt the fable given by the function get_fable_string().
    Once you decrypt the message, be sure to include the fable
    as a comment at the end of this problem set.
    returns: string - fable in plain text
    """
    ### TODO.
    
#What is the fable?
#
#
#
#
#
