# See LICENCE file for copyright and licence details

import json
import collections
import colour

def read_data(file):
    with open(file, "r") as f:
        data = json.load(f)
    return data

def write_data(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def print_dict(name, dictionary, amount):
    dictionary = dict(collections.OrderedDict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True)))
    print(f"\n{colour.blue}{name}{colour.end}")
    for k, v in list(dictionary.items())[:amount]:
        print(f"  {colour.cyan}{k}{colour.end}: {colour.green}{v}{colour.end}")
    print()