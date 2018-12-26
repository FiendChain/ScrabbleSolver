import json
import os
import argparse

DEFAULT_CHAR_SET = "0123456789abcdefghijklmnopqrstuvwxyz-?"
DEFAULT_WORD_COUNTS = {'counts': {}, 'char_set': DEFAULT_CHAR_SET}

def get_count(word):
    count = {}
    for char in word.lower():
        count.setdefault(char, 0)
        count[char] += 1
    return count

def add_word(word, counts):
    count = get_count(word)    
    curr_count = counts['counts']
    char_set = counts['char_set']

    for char in char_set:
        # if char not in count set in 0
        char_count = count.get(char, 0)
        default_value = {} if char is not char_set[-1] else []
        curr_count = curr_count.setdefault(str(char_count), default_value)
    if word not in curr_count:
        curr_count.append(word)
        return True
    return False

def generate_counts(words, word_counts=DEFAULT_WORD_COUNTS.copy()):
    for word in words:
        add_word(word, word_counts)
    return word_counts

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    parser.add_argument('--override', action='store_true')
    parser.add_argument('--char_set', default=DEFAULT_CHAR_SET)
    args = parser.parse_args()

    if not args.override:
        with open(args.output, 'r') as output_file:
            try:
                word_counts = json.load(output_file)
            except json.JSONDecodeError:
                word_counts = {'counts': {}, 'char_set': args.char_set}
    else:
        word_counts = {'counts': {}, 'char_set': args.char_set}
    
    with open(args.input, 'r') as input_file:
        for lines in input_file.readlines():
            words = lines.rstrip('\n').split(' ')
            for word in words:
                add_word(word, word_counts)
                
    with open(args.output, 'w') as output_file:
        json.dump(word_counts, output_file)

if __name__ == '__main__':
    main()
