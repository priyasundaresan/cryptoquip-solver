""" Solver for cryptoquip puzzles commonly found in newspapers:
eg. (unsolved): PSXCI ECHGOCO BEPLX HCA-OXTZXUXA ABXWWXUL PJOXI ZCUOGSGZCOX GI LKYCHHWXL: C KYCUUXW UXXJ.
    (solved): OCEAN HABITAT WHOSE BAD-TEMPERED DWELLERS OFTEN PARTICIPATE IN SQUABBLES: A QUARREL REEF. """

import re # Used to remove punctuation from a puzzle
import string # Used to get a list of letters A-Z
import argparse # Used to get puzzle input at the command line
import pprint # Used to print out test cases nicely
import time # Used to calculate how quickly puzzle is solved

""" Import tests – stored as a dictionary of the form:
testCaseNumber: [encryptedMessage, decryptedMessage] """
tests = open('cryptotests.txt', 'r')
contents = [i for i in [x.strip() for x in tests.readlines()] if i]
nums = [int(i[:-1]) for i in contents if not contents.index(i)%3]
unsolved = [i for i in contents if contents.index(i)%3 == 1]
solved = [i for i in contents if contents.index(i)%3 == 2]
testsCache = {nums[i]: [unsolved[i], solved[i]] for i in range(len(nums))}

""" Import frequency table for English words """
file = open('wordsByFrequency.txt', 'r')
frequencyTable = {word: frequency for (frequency, word) in list(enumerate([word.strip() for word in file.readlines()]))}
file.close()

WORDS = list(frequencyTable.keys())
LETTERS = string.ascii_uppercase

""" Used to parse encrypted message and remove punctuation """
PUNCTUATION = re.compile('[^A-Z\s]')

def removePunctuation(message):
    """ Note: hyphenated words are broken into two words (typically they involve some sort of pun, and are best considered separately) """
    newMessage = ''
    for ch in message:
        if ch in ['-','–']:
            newMessage += ' '
        else:
            newMessage += ch
    return PUNCTUATION.sub('', newMessage)

def hashWord(word):
    """ Generates the canonical form of a word; 'HELLO' -> 'ABCCD' """
    seen = {}
    i = 0
    pattern = []
    for ch in word:
        if ch in seen:
            pattern.append(seen[ch])
        else:
            seen[ch] = LETTERS[i]
            pattern.append(seen[ch])
            i += 1
    return ''.join(pattern)

""" Stores a dictionary of canonical forms and the words they represent. """
def generateWordHash(dictionarySize=len(WORDS)):
    wordHash = {}
    for word in WORDS[:dictionarySize]:
        pattern = hashWord(word)
        if pattern in wordHash:
            wordHash[pattern] += [word]
        else:
            wordHash[pattern] = [word]
    return wordHash
wordHash = generateWordHash()

def decryptMessage(letterMap, encryptedMessage):
    """ Given a letter Map, decrypts an encrypted message by substitution. """
    transMap= letterMap.copy()
    for key in transMap:
        if not transMap[key]:
            transMap[key] = '.'
    translated = ''
    for symbol in encryptedMessage:
        if symbol in transMap:
            translated += transMap[symbol]
        else:
            translated += symbol
    return ''.join(translated)

""" Generates a blank letterMapping. """
blankMap = lambda: {letter: '' for letter in string.ascii_uppercase}

def sortCipherwords(cipherwordList):
    """ Sort a cipherwordList in descending order of length of cipherword. """
    cipherwordList = [i for i in cipherwordList if hashWord(i) in wordHash]
    return sorted(cipherwordList, key=lambda cipherword: -len(cipherword))

def sortCandidates(candidates):
    """ Sort a list of candidates for a cipherword in order of their frequency (least frequent come first, to
    eliminate bad guesses early)."""
    sortedByFrequency = sorted(candidates, key=lambda candidate: frequencyTable[candidate])
    return sortedByFrequency

def consistent(letterMap, cipherword, candidate):
    """ Given a letterMap, a cipherword, and a candidate for the cipherword,
        check whether the letterMap is consistent with the new cipherword/candidate pairwise by letter. If it is,
        update the letterMap. """
    for cipherletter, letter in zip(cipherword, candidate):
        mapped = letterMap[cipherletter]
        if (mapped and (mapped != letter)):
            return None
        if (not mapped) and (letter in letterMap.values()):
            return None
    return mergeMaps(letterMap, cipherword, candidate)

def mergeMaps(letterMap, cipherword, candidate):
    """ Extend a current letter map by mapping all of the characters in cipherword to corresponding
        characters in candidate word. """
    letterMap = letterMap.copy()
    for cipherletter, letter in zip(cipherword, candidate):
        letterMap[cipherletter] = letter
    return letterMap

def solve(letterMap, score, cipherwordList):
    """ For each cipherword, try to extend a letterMap by checking it against each candidate.
        Also consider the case where a cipherword doesn't map to a word in our dictionary (i.e. proper nouns, puns, non-English words).
        To account for this case, we additionally pass in the current letterMapping and move on to next cipherword entirely."""
    global bestScore
    """ If the current number of words solved + the number of remaining cipherwords to be solved
    cannot beat the current best score, return """
    if bestScore > score + len(cipherwordList):
        return
    """ If there are no remaining cipherwords, print the best translation or the current translation if
    it is even better """
    if len(cipherwordList) == 0:
        if score >= bestScore:
            print(decryptMessage(letterMap, message))
            bestScore = score
        return
    canonical = hashWord(cipherwordList[0])
    for candidate in sortCandidates(wordHash[canonical]):
        newMap = consistent(letterMap, cipherwordList[0], candidate)
        if newMap:
            solve(newMap, score + 1, cipherwordList[1:])
    solve(letterMap, score, cipherwordList[1:])

""" To run the program at the command line.
    eg 1) $ python3 cryptoquip.py -t 90 # Solves test case 90
    eg 2) $ python3 cryptoquip.py -c # Prints out all test cases """
parser = argparse.ArgumentParser(description='Solve a Cryptoquip')
parser.add_argument('-t', '--test', type=int, metavar='', help='enter a test case puzzle | (eg: -t 99) runs test 99')
parser.add_argument('-s', '--size', type=int, metavar='', help='enter a limit (< 9897) on dict size | (eg: -s 1000) uses a 1K word dict')
# Note: experiment with dictionary size to test program speed/play with how small the dictionary can get before it cannot solve puzzles
# Sometimes even <1000 word dictionary is all that is needed; ~2000-5000 usually works!
parser.add_argument('-c', '--cases', action='store_true', help='print all test cases and solutions')
parser.add_argument('-i', '--input', action='store_true', help='enter puzzle input directly')
args = parser.parse_args()

""" Gets a puzzle from user, parses and orders cipherwords, and solves puzzle."""
if __name__ == '__main__':
    if args.cases:
        pprint.pprint(testsCache) # Prints the suite of test cases
    else:
        if args.input:
            message = input("Enter a puzzle here: \n")
        elif args.test:
            message = testsCache[args.test][0]
        if args.size:
            wordHash = generateWordHash(args.size)
        cipherwordList = sortCipherwords(removePunctuation(message).split())
        bestScore = 0 # 0 words are solved to begin with; this updates/increases as puzzle is solved; translations that beat this score are printed
        start = time.time()
        try:
            solve(blankMap(), 0, cipherwordList)
            print("\n" + "Solved in: ", (time.time() - start), 's')
        except KeyboardInterrupt: # Sometimes puzzles don't converge but are basically solved besides 1 or 2 letters; interrupt to see time elapsed
            print("\n" + "Solved in: ", (time.time() - start), 's')
