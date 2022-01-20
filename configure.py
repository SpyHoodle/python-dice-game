# See LICENSE file for copyright and licence details
# Github: https://github.com/SpyHoodle/python-dice-game

# Import custom file
import colour as c


def player_amount():
    # Loop is used to keep ask again if an invalid answer is entered
    while True:
        # Ask for the number of players
        num_players = input(f"{c.cyan}How many players? (2 or more): {c.end}")

        # The number of players has to be a number
        if num_players.isnumeric() is False:
            # Tell the user that the input is not numeric
            print(f"{c.red}Error: Invalid input, not numeric{c.end}")

        # There must be more than 2 players
        elif int(num_players) < 2:
            # Tell the user that the input is less than 2
            print(f"{c.red}Error: Amount of players is less than 2{c.end}")

        else:
            # Return the number of players as an integer
            return int(num_players)


def rounds_amount():
    # Loop is used to keep ask again if an invalid answer is entered
    while True:
        # Ask for the number of rounds
        rounds = input(f"{c.cyan}How many rounds? (1 or more): {c.end}")

        # The number of rounds has to be a number
        if rounds.isnumeric() is False:
            print(f"{c.red}Error: Invalid input, not numeric{c.end}")

        # There must be more than 1 rounds
        elif int(rounds) < 1:
            # Tell the user that the input is less than 1
            print(f"{c.red}Error: Amount of rounds is less than 1{c.end}")

        else:
            # Return the number of rounds as an integer
            return int(rounds)


def configure_game():
    # Get the number of players and number of rounds
    num_players, rounds = player_amount(), rounds_amount()
    # Return the number of players and the number of rounds
    return num_players, rounds
