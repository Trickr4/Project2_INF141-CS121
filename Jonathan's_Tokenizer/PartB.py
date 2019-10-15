from collections import defaultdict
import sys

"""
Arguements: Open text file.
Return: List on search tokens.
Reads a text file and splits each line into
word(tokens) and puts the words in a list.
Time Complexity: O(n^2)
"""
def tokenize(file: open) -> []:
    x = []
    for line in file:
        for word in line.split():
            word = word.strip(".?!,")
            if word.isalnum():
                x.append(word)
            else:
                token = word
                for letter in word:
                    ascii_num = ord(letter)
                    if ((ascii_num > 47 and ascii_num < 58) or \
                        (ascii_num > 64 and ascii_num < 91) or \
                        (ascii_num > 96 and ascii_num < 123)) == False:
                        if token.split(letter,1)[0] != '':
                            x.append(token.split(letter,1)[0])
                        token = "".join(token.split(letter,1)[1:])
                if token.isalnum() == True:
                    x.append(token)
    return x

"""
Arguements: List of tokens.
Return: Defaultdict(int) of word frequencies.
Compiles a list into a default dictionary with the
tokens as keys and the token frequencies as values.
Time Complexity: O(n)
"""
def computeWordFrequencies(token_list: [""]) -> defaultdict(int):
    x = defaultdict(int)
    for word in token_list:
        x[word] += 1
    return x

"""
Arguements: Defaultdict(int) of word frequencies.
Return: NULL.
Prints the token and their number of frequencies.
Time Complexity: O(n)
"""
def print_WordFrequencies(x: defaultdict(int)):
    for token in sorted(x.items(), key = lambda x: (x[1], x[0]) ,reverse = True):
        print(token[0] + ": " + str(token[1]))

"""
Arguements: 2 Defaultdict(int) of word frequencies.
Return: The intersection of defaultdict(int) of word frequencies.
Puts the 2 Arguements in a set intersection. Then the set
is put in a defaultdict(int) with the the values being the sum of
the 2 arguements' keys.
Time Complexity: O(n)
"""
def commonWordFrequencies(x: defaultdict(int), y: defaultdict(int) ) -> defaultdict(int):
    same = defaultdict(int)
    common = set( x.keys() ) & set( y.keys() )
    for word in common:
        same[word] = x[word] + y[word]
    return same

"""
Arguements: Defaultdict(int) of common word frequencies.
Return: NULL.
Prints the token and their number of frequencies.
Time Complexity: O(n)
"""
def print_CommonWordFrequencies(x: defaultdict(int)):
    for token in x:
        print(token)    
    print( str(len(x)) )

if __name__ == '__main__':
    x = computeWordFrequencies(tokenize(open(sys.argv[1] )))
    y = computeWordFrequencies(tokenize(open(sys.argv[2] )))
    print_CommonWordFrequencies(commonWordFrequencies(x, y))
