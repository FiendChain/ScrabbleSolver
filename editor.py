import json
import argparse
from parse_json import add_word, get_count, DEFAULT_WORD_COUNTS
from scrabble import fetch_anagram

class EditorModes:
    ADD = '+'
    DELETE = '-'
    ANAGRAM = '*'

class EditorCommand:
    def __init__(self, cmd_str, func, help):
        self.cmd_str = cmd_str
        self.func = func
        self.help = help
    
    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)

    def __str__(self):
        return '{}: {}'.format(self.cmd_str, self.help)

class Editor:
    def __init__(self):
        self.commands = {}
        self.modes = {}
        self.mode = EditorModes.ADD
        self.word_counts = DEFAULT_WORD_COUNTS.copy() 
        self.filename = None
        self.made_changes = False
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            line = input('{} '.format(self.mode))
            line = line.rstrip(' ')
            words = line.split(' ')
            cmd_str = words[0]
            args = words[1:]
            if cmd_str in self.commands:
                try:
                    self.commands[cmd_str](self, *args)
                except TypeError as ex:
                    print(str(ex))
            else:
                self.modes[self.mode](cmd_str, self.word_counts)
            
    def register_mode(self, mode):
        def decorator(func):
            self.modes[mode] = func
            return func
        return decorator

    def register_command(self, cmd_str, help=None):
        def decorator(func):
            command = EditorCommand(cmd_str, func, help)
            self.commands[cmd_str] = command
            return func
        return decorator

    def load(self, filename=None):
        filename = filename if filename else self.filename
        if not filename:
            print('No file to load from!')
            return
        with open(filename, 'r') as file:
            self.word_counts = json.load(file)
        self.filename = filename

    def save(self, filename=None):
        filename = filename if filename else self.filename
        if not filename:
            print('No file to save to!')
            return
        print('Saving to \'{}\''.format(self.filename))
        with open(filename, 'w') as file:
            json.dump(self.word_counts, file)
        self.made_changes = False
        self.filename = filename

    def set_mode(self, mode):
        self.mode = mode

    def help(self):
        for cmd_str, command in self.commands.items():
            print(command)
    
    def close(self):
        self.running = False
        if self.made_changes:
            print('[Warning] Unsaved changes')
            response = input('Press y to continue without saving, otherwise save to \'{}\'\n'.format(self.filename))
            if response not in ('y', 'Y'):
                self.save()

class DefaultEditor(Editor):
    def __init__(self, threshold=10):
        super().__init__()
        self.register_command('!add', '+ Add entry')(lambda cls: Editor.set_mode(cls, EditorModes.ADD))
        self.register_command('!del', '- Remove entry')(lambda cls: Editor.set_mode(cls, EditorModes.DELETE))
        self.register_command('!chk', '* Switch to anagram mode')(lambda cls: Editor.set_mode(cls, EditorModes.ANAGRAM))
        self.register_command('!threshold', 'Set threshold for anagram mode')(DefaultEditor.set_threshold)
        self.register_command('!help')(Editor.help)
        self.register_command('!quit')(Editor.close)
        self.register_command('!save')(Editor.save)

        self.register_mode(EditorModes.ADD)(self.add_word)
        self.register_mode(EditorModes.DELETE)(self.delete_word)
        self.register_mode(EditorModes.ANAGRAM)(self.show_anagrams)

        self.threshold = threshold

    def set_threshold(self, threshold):
        try:
            threshold = int(threshold)
            self.threshold = threshold
        except ValueError:
            print('{} is not a valid threshold'.format(threshold))

    def add_word(self, word, word_counts):
        if add_word(word, word_counts):
            self.made_changes = True

    def delete_word(self, word, word_counts):
        if delete_word(word, word_counts):
            self.made_changes = True

    def show_anagrams(self, word, word_counts):
        anagrams = fetch_anagram(word, word_counts)
        print(anagrams[:self.threshold])

def delete_word(word, counts):
    count = get_count(word)    
    curr_count = counts['counts']
    char_set = counts['char_set']

    for char in char_set:
        # if char not in count set in 0
        char_count = count.get(char, 0)
        if str(char_count) in curr_count:
            curr_count = curr_count[str(curr_count)]
        return

    try:
        curr_count.remove(word)
        return True
    except ValueError:
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='file')
    args = parser.parse_args()

    editor = DefaultEditor()
    editor.load(args.file)
    editor.run() 

if __name__ == '__main__':
    main()

