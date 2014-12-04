from os import makedirs
from os.path import (
    expanduser,
    exists,
    join
)

from dragonfly import Choice

user_choices_dir = join(expanduser("~"), ".dragonfly")

def combine_choices(*choices):
    return dict([i
                 for c in choices
                 for i in (c._choices.items()
                           if isinstance(c, Choice)
                           else c.items())])

def parse_user_choices(choices):
    result = dict()
    
    if not ensure_directory(user_choices_dir):
        return result

    user_choices_file = join(user_choices_dir, choices)
    if not exists(user_choices_file):
        return result

    with open(user_choices_file, 'r') as f:
        for line in f:
            mapping = line.split(":", 1)
            result[mapping[0].strip()] = mapping[1].strip()

    return result
    
def ensure_directory(directory):
    if not exists(directory):
        makedirs(directory)
    return exists(directory)
