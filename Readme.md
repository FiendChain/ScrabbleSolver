# Description
Each *.json file has a character set and a nested dictionary of character counts.
For instance, the character set "a..z" will have a nested dictionary 26 layers deep.
Each layer of the dictionary will have keys associated with the character count of the word.
The final datastructure will behave like a tree, which can be traversed downwards according to the characterThis works on a similar principle to Huffman coding, where the character count is of the word is used
set used to create it, via the character count of the word.

To get solutions to a scrabble problem, the word count of the anagram is calculated, and then is used to traverse down
the appropriate branches of the tree. 
To get any words inside the anagram, the algorithm would recursively traverse down the branches of the tree, where the character count of that specific
character is equal of less than the actual count.

## Example
```python
# apple
count = { 'a': 1, 'p': 2, 'l':1, 'e': 1 }
# The converted entry will be a nest dict with character counts
#                  a   b   c   d   e  f-k  l  m-o  p  q-y  z  
converted_count = {1: {0: {0: {0: {1: ... {1: ... {2: ... {0: ['apple']}}}}}}}}
# Since each tree will be constructed differently according to the character set that is used,
# it must be stored along the tree to allow for traversal
```

## Computational complexity
```
n = length of character set
k = length of word

# Assuming each recursion can be done inside another thread
Worst complexity = n = O(n) # Each branch will be handled concurrently with other branches
Best complexity  = n = O(n)

# Assuming recursion via the stack, without multithreading
# If the character count is 'm' for a branch, then that branch will create 'm' branches
# This is assuming that each of those 'm' branches will have an associated word along that path, which is highly unlikely
# E.g. If the character set is a..z, then the character count would be a0, a1, etc
Worst complexity = a0*a1*a2*...*a_n*(n-k)
If k = m!,
Worst complexity = m!*(n-k) = O(m!)
```
<a href="https://www.codecogs.com/eqnedit.php?latex=Length&space;=&space;\sum_{k=0}^{n-1}{A_k}\newline&space;Complexity&space;=&space;(n-Length)*\prod_{k=0}^{n-1}{A_k}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Length&space;=&space;\sum_{k=0}^{n-1}{A_k}\newline&space;Complexity&space;=&space;(n-Length)*\prod_{k=0}^{n-1}{A_k}" title="Length = \sum_{k=0}^{n-1}{A_k}\newline Complexity = (n-Length)*\prod_{k=0}^{n-1}{A_k}"/></a>
```
# Best case occurs when all the character counts are 1, or all in one character
# For one character at most
Best complexity (1 char) = n+(n-1)+...+(n-k) = k/2 (2n+(k-1)(-1)) = k/2 (2n-k+1)

# For the worst case of this best case, k = n (max characters), which is unlikely
Best complexity (1 char) = n/2 (2n-n+1) = n^2/2 = O(n^2)

# Or the normal expected case where k != n
Best complexity (1 char) = n*k + k^2/2 - k/2 = O(k^2)

# This all assumes that each branch for each character count exists, which is unlikely, meaning actual complexity would be even lower than this
```

# Usage
```bash
# [] = optional, <> = required
# To run the scrabble editor, and will load counts.json by default
python3 scrabble.py [file]
# To edit the json file
python3 editor.py <file>
# To generate json file from a list of words (dictionary)
python3 parse_json.py <input> <output> [--override] [--char_set STRING]
```