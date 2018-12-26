import json
from parse_json import get_count
import argparse

def recursive_fetch(anagram_count, counts, char_set, level=0, exact=False):
    # if last level, must contain list
    if level == len(char_set):
        return counts
    char_count = anagram_count.get(char_set[level], 0)
    matches = []
    if not exact:
        for count in range(char_count, -1, -1):
            if str(count) in counts:
                matches.extend(recursive_fetch(anagram_count, counts[str(count)], char_set, level+1, exact=exact))
    elif char_count in counts:
        matches.extend(recursive_fetch(anagram_count, counts, char_set, level+1))

    return matches


def fetch_anagram(anagram, word_counts, exact=False):
    anagram_count = get_count(anagram)
    counts = word_counts['counts']
    char_set = word_counts['char_set']
    matches = recursive_fetch(anagram_count, counts, char_set, exact=exact)
    matches = sorted(matches, key=lambda word: len(word), reverse=True)
    return matches

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--counts', default='counts.json')
    parser.add_argument('--threshold', type=int, default=10) # top 10 words
    args = parser.parse_args()

    with open(args.counts, 'r') as file:
        word_counts = json.load(file)

    while True:
        anagram = input('Enter anagram: ')
        anagrams = fetch_anagram(anagram, word_counts)
        print(anagrams[:args.threshold])

if __name__ == '__main__':
    main()
