# cryptoquip-solver
A solver for newspaper cryptoquip puzzles like [this one](https://cryptoquipanswer.com/2018/04/06/cryptoquip-answer-for-4-6-18/).

## Files
* cryptoquip.py – the solve algorithm
* cryptotests – contains cryptoquip test cases
* wordsByFrequency – a list of words sorted by frequency (a utility to cryptoquip.py)

## Download
```
$ git clone https://github.com/priyasundaresan/cryptoquip-solver
```

## Dependencies
* pprint – "pretty prints" output
* argparse – command line utility for running various test cases; see usage
```
$ pip install pprint
$ pip install argparse
```

## Usage
You can run any of the puzzles listed in cryptotests or your own puzzles.
Navigate to the folder containing the above files and run any of the following options in the terminal:

### To run test #99 from cryptotests, run:
```
$ python3 cryptoquip.py -t 99
```
By default the program tries to solve the encrypted puzzle by decoding each cipherword to a word in a stored dictionary. The default dictionary size is just over 9,000 words. You may want to experiment with the size of the dictionary used if the solve program is taking too long or if you want to test how small the dictionary can get while still dciphering a puzzle.

### To run test #99 from cryptotests with a dictionary size of 2000, run:
```
$ python3 cryptoquip.py -t 99 -s 2000
```
### To enter your own test into the shell directly, run:
```
$ python3 cryptoquip.py -i
```
You can optionally limit the size of the dictionary (ex: 4000) as well by running:
```
$ python3 cryptoquip.py -i -s 4000
```

And you will be prompted as follows:
```
Enter a puzzle here:
```
### You can also add a puzzle as test XXX into the plaintext file cryptotests, like this:
```
XXX.
ENCRYPTED PUZZLE
```

And run:
```
$ python3 cryptoquip.py -t XXX
```
### To view all cases on cryptotests, run:
```
$ python3 cryptoquip.py -c
```
