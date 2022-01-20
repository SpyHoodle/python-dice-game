# See licence file for copyright and licence details
# Github: https://github.com/spyhoodle/python-dice-game

# Import needed libraries
import json
import collections
import colour


def read_data(file):
    # Open the game data file
    with open(file, "r") as f:
        # Load the json file as a dictionary
        data = json.load(f)
    # Return the game data dictionary
    return data


def write_data(data, file):
    # Open the game data file
    with open(file, "w") as f:
        # Write the dictionary game data to the file
        json.dump(data, f, indent=2)


def print_dict(name, dictionary, amount):
    # Sort the dictionary
    dictionary = dict(collections.OrderedDict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True)))
    # Print the title of the dictionary
    print(f"{colour.blue}{name}{colour.end}")
    # Print out the dictionary contents using a loop
    for k, v in list(dictionary.items())[:amount]:
        # Print out the key: value
        print(f"  {colour.cyan}{k}{colour.end}: {colour.green}{v}{colour.end}")
    # New line (blank print() statement)
    print()
