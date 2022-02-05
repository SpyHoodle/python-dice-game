# See LICENSE file for copyright and licence details
# Github: https://github.com/spyhoodle/python-dice-game

#  ____        _   _                   ____  _
# |  _ \ _   _| |_| |__   ___  _ __   |  _ \(_) ___ ___
# | |_) | | | | __| '_ \ / _ \| '_ \  | | | | |/ __/ _ \
# |  __/| |_| | |_| | | | (_) | | | | | |_| | | (_|  __/
# |_|    \__, |\__|_| |_|\___/|_| |_| |____/|_|\___\___|
#        |___/
#   ____
#  / ___| __ _ _ __ ___   ___
# | |  _ / _` | '_ ` _ \ / _ \
# | |_| | (_| | | | | | |  __/
#  \____|\__,_|_| |_| |_|\___| v2.2

# Import needed libraries
import random
import time
import os

# Import custom files
import colour as c
import userdata
import players
import configure


# The Game class - the main class for the Game
class Game:
    def __init__(self, num_players=2, rounds=5):
        # Development mode - Enables extra functions
        self.dev_mode = True
        # The number of players
        self.num_players = num_players
        # The number of rounds
        self.rounds = rounds
        # The data file to read from
        self.data_file = "pdg-data.json"
        # A dictionary of concurrent players
        self.playing = {}

    def roll(self):
        # Press enter to roll the dice
        input(f"{c.green}Press enter to roll{c.end}")
        # The result will write over this (\r)
        print("Rolling...", end="\r")
        # Wait 0.5 seconds
        time.sleep(0.5)
        # Random Number acts as the die
        roll = random.randint(1, 6)
        # Show result (roll)
        print(f"You rolled a: {roll}\n")

        # Return result (roll)
        return roll

    def turn(self, player, score, extra=False):
        # Print the player's name
        print(f"{c.blue}Player: {player}{c.end}")
        # Print the player's score
        print(f"{c.blue}Score: {self.playing[player]}{c.end}\n")
        # Roll 2 times, if turn is extra then the player only rolls once
        rolls = [self.roll() for _ in range(1 if extra is True else 2)]

        # If turn isn't the extra (players haven't drew)
        if extra is False:
            # If both rolls are the same (a double)
            if rolls[0] == rolls[1]:
                # Tell the user they rolled a double
                print(f"{c.cyan}You rolled a double!{c.end}")
                # Add the roll to the rolls list, which is the bonus
                rolls.append(self.roll())
                # The bonus message for the double
                bonus_msg = f"{c.green}+{rolls[-1]}{c.end} (double roll)"

            elif sum(rolls) % 2:
                # The bonus for an odd total is -5
                bonus_msg = f"{c.red}-5{c.end} (odd score)"
                # Add the bonus to the end of the rolls list
                rolls.append(-5)

            else:
                # The bonus for an even total is +10
                bonus_msg = f"{c.green}+10{c.end} (even score)"
                # Add the bonus to the end of the rolls list
                rolls.append(10)

            # Wait one second
            time.sleep(1)
            # Show the score, without the bonus
            print(f"Score: {c.green}{rolls[0]} + {rolls[1]}{c.end} = {c.blue}{sum(rolls[0:2])}{c.end}")
            # Wait one second
            time.sleep(1)
            # Show the bonus to the player
            print(f"Bonus: {c.green if rolls[-1] > 0 else c.red}{bonus_msg}{c.end}")
            # Wait one second
            time.sleep(1)

            # Print the total score, which shows the math used
            print("Total: " +
                  f"{c.red}{score}{c.end} " +
                  f"{c.green}+{sum(rolls[0:2])}{c.end} " +
                  f"{c.green if rolls[-1] > 0 else c.red}{'+' if rolls[-1] > 0 else ''}{rolls[-1]}{c.end} " +
                  f"= {c.blue}{max(0, score + sum(rolls))}{c.end}\n\n")

        # Return the total score earned this turn
        return sum(rolls)

    def round(self, round):
        # Clear the screen
        os.system("clear")

        # If round is sudden death
        if round == "sudden_death":
            # Print the round name "Sudden Death"
            print(f"{c.magenta}Round: Sudden Death!{c.end}")
            # Run for the amount of concurrent players
            for player in self.playing.keys():
                # The player's score is the value returned turn()
                # Extra turn is needed here as each player only rolls once
                self.playing[player] += self.turn(player, self.playing[player], extra=True)
                # Wait for 1 second
                time.sleep(1)

        # Default round style
        else:
            # Print the round number
            print(f"{c.magenta}Round {round+1}:{c.end}")
            # Run for the amount of concurrent players
            for player in self.playing.keys():
                # The player's score is the value returned turn()
                self.playing[player] += self.turn(player, self.playing[player])
                # Set the players score to 0 if it becomes negative
                self.playing[player] = max(0, self.playing[player])
                # Wait for 1 second
                time.sleep(1)

        # Press enter to continue
        input(f"{c.green}Press enter to continue...{c.end}")

    def game_over(self):
        # Find the winner
        winner = {"username": max(self.playing, key=self.playing.get), "score": max(self.playing.values())}
        # Clear the screen
        os.system("clear")
        # Print the winner
        print(f"{c.green}Game over! The winner is '{max(self.playing, key=self.playing.get)}'!{c.end}\n")
        # Show a maximum of 10 scores on screen
        score_amount = 10 if self.num_players > 10 else self.num_players
        # Print out the scores for this game
        userdata.print_dict(f"Scores this game (Top {score_amount}):", self.playing, score_amount)

        # Read from the data file
        data = userdata.read_data(self.data_file)
        # Add the winner to the score history
        data["scores"].append(winner)
        # Write to the data file
        userdata.write_data(data, self.data_file)

        # Print out top 5 previous high scores
        scores = {i["username"]: i["score"] for i in data["scores"]}
        userdata.print_dict("Highscores (Top 5):", scores, 5)


# Create the Game() object with default values
game = Game()


def user_manager():
    # User manager menu title
    print(f"\n{c.blue}User Manager:{c.end}")
    # Show menu options (one line)
    print(f"{c.cyan}(C){c.end}reate player, " +
          f"{c.cyan}(D){c.end}elete player, " +
          f"{c.cyan}(E){c.end}dit password, " +
          f"or {c.cyan}(R){c.end}eturn to menu:")

    # Ask for an input for the menu
    choice = input("> ").upper()

    if choice == "C" or choice == "CREATE" or choice == "CREATE PLAYER":
        # Create a new player
        players.new_user(game.data_file)

        # Return to user_manager() menu
        user_manager()

    elif choice == "D" or choice == "DELETE" or choice == "DELETE PLAYER":
        # Delete a player
        players.del_user(game.data_file)

        # Return to user_manager() menu
        user_manager()

    elif choice == "E" or choice == "EDIT" or choice == "EDIT PASSWORD":
        # Change password
        players.change_pass(game.data_file)

        # Return to user_manager() menu
        user_manager()

    elif choice == "R" or choice == "RETURN" or choice == "RETURN TO MENU":
        # Don't return to user_manager() menu
        print(f"{c.red}Returning to main menu...{c.end}\n")

    else:
        # Choice from the menu is not found
        print(f"{c.red}Error: Command not recognized{c.end}")

        # Return to user_manager() menu
        user_manager()


# Main menu function
def menu():
    # Create the game object with default values
    game = Game()

    # Main menu title
    print(f"{c.blue}Main Menu:{c.end}")
    # Menu options
    print(f"{c.cyan}(S){c.end}tart a game, " +
          f"{c.cyan}(M){c.end}anage players, " +
          f"{c.cyan}(V){c.end}iew highscores, " +
          f"or {c.cyan}(E){c.end}xit:")

    # Ask for an input for the menu
    choice = input("> ").upper()

    if choice == "S" or choice == "START" or choice == "START A GAME":
        # Print a title for configuring the game
        print(f"{c.blue}Configure the game before starting:{c.end}")
        # Configure the game
        num_players, rounds = configure.configure_game()

        # Create a Game() object with the game settings
        game = Game(num_players=num_players, rounds=rounds)

        # Run for the amount of players
        for i in range(game.num_players):
            # Login a user
            game.playing = players.login_user(game.playing, game.data_file)

        # Countdown for 3 seconds
        for i in [3, 2, 1]:
            # Countdown will write over itself (\r)
            print(f"{c.magenta}The game will start in {i}...{c.end}", end="\r")
            # Wait 1 second
            time.sleep(1)

        # Run for the amount of rounds specified
        for round in range(game.rounds):
            # Create a round and pass the round number
            game.round(round)

        # While all the players have the same score
        while all(element == list(game.playing.values())[0] for element in game.playing.values()):
            # Tell the players they have the same score
            print(f"{c.green}All players have the same score!{c.end}")
            # Wait 1 second
            time.sleep(1)
            # Create a Sudden Death round
            game.round("sudden_death")

        # Game over sequence
        game.game_over()

        # Return to main menu
        menu()

    elif choice == "M" or choice == "MANAGE" or choice == "MANAGE PLAYERS":
        # Manage players menu (recursive function)
        user_manager()

        # Return to main menu
        menu()

    elif choice == "V" or choice == "VIEW" or choice == "VIEW HIGHSCORES":
        # Clear the screen
        os.system("clear")
        # Read data from the data file
        data = userdata.read_data(game.data_file)
        # Print out top 5 previous highscores
        scores = {i["username"]: i["score"] for i in data["scores"]}
        userdata.print_dict("Highscores (Top 5):", scores, 5)

        # Return to main menu
        menu()

    elif choice == "C" or choice == "CLEAR":
        # Clear the screen
        os.system("clear")

        # Return to main menu
        menu()

    elif choice == "E" or choice == "EXIT":
        # Say goodbye, and don't return to main menu
        print(f"{c.red}Goodbye!{c.end} Thank you for playing!")

    else:
        # Choice from the menu is not fouind
        print(f"{c.red}Error: Command not recognized{c.end}\n")

        # Return to main menu
        menu()


# Fist game startup!
def startup():
    # Clear the screen
    os.system("clear")

    # Check whether a pdg-data.json file is present
    if os.path.exists("pdg-data.json") is False:
        # Tell the user that a pdg-data file isn't present
        print(f"{c.red}Important: No pdg-data.json (game data) file found.{c.end}")
        # Yes or no, no will quit the game as pdg NEEDS game data
        choice = input("Would you like to create one? (y/N): ").upper()

        if choice == "Y" or choice == "YES":
            # Tell the user we're creating the file
            print(f"{c.yellow}Creating game data...{c.end}")
            # Create a new file called pdg-data.json
            with open('pdg-data.json', 'w') as file:
                # Write a json format for python-dice-game
                file.write('{\n"scores": []\n}')

            # Tell the user we've succeeded
            print(f"{c.green}Game data created!{c.end}")

            # Wait 1 second
            time.sleep(1)

            # Print out a welcome message
            print(f"{c.magenta}Welcome to Python Dice Game{c.end} {c.green}v2.1!{c.end}" +
                  f"{c.red}{' (Development Mode)' if game.dev_mode == True else ''}{c.end}")

            # Start the main menu (recursive function)
            menu()
        else:
            # Tell the user the game is quitting because it needs game data
            print(f"{c.red}Quitting game... (PDG needs game data){c.end}")
    else:
        # Print out a welcome message
        print(f"{c.magenta}Welcome to Python Dice Game{c.end} {c.green}v2.1!{c.end}" +
              f"{c.red}{' (Development Mode)' if game.dev_mode == True else ''}{c.end}")

        # Start the main menu (recursive function)
        menu()


# Prevent running if imported by another file.
if __name__ == "__main__":
    # Start the game
    startup()
