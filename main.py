# See LICENCE file for copyright and licence details
# Github: https://github.com/SpyHoodle

#   ____        _   _                   ____  _
# |  _ \ _   _| |_| |__   ___  _ __   |  _ \(_) ___ ___
# | |_) | | | | __| '_ \ / _ \| '_ \  | | | | |/ __/ _ \
# |  __/| |_| | |_| | | | (_) | | | | | |_| | | (_|  __/
# |_|    \__, |\__|_| |_|\___/|_| |_| |____/|_|\___\___|
#        |___/
#   ____
#  / ___| __ _ _ __ ___   ___
# | |  _ / _` | '_ ` _ \ / _ \
# | |_| | (_| | | | | | |  __/
#  \____|\__,_|_| |_| |_|\___| v2.1

# Import needed libraries
import random
import time
import os

# Import custom files
import colour
import userdata
import players
import configure

class Game:
    def __init__(self, num_players=2, rounds=5):
        self.dev_mode = True # Development mode - Enables extra functions
        self.num_players = num_players # The nuber of players
        self.rounds = rounds # The number of rounds
        self.data_file = "data.json" # The data file to read from
        self.playing = {} # A dictionary of concurrent players

    def roll(self):
        input(f"{colour.green}Press enter to roll{colour.end}") # Press enter to roll the dice

        print("Rolling...", end="\r") # The result will write over this (\r)
        time.sleep(0.5) # Wait 0.5 seconds
        roll = random.randint(1, 6) # Random Number acts as the die

        print(f"You rolled a: {roll}\n") # Show result
        return roll

    def turn(self, player, score, extra=None):
        print(f"{colour.blue}Player: {player}{colour.end}") # Print the player's name
        print(f"{colour.blue}Score: {self.playing[player]}{colour.end}\n") # Print the player's score
        rolls = [self.roll() for _ in range(1 if extra == "extra" else 2)] # Roll 2 times, if turn is "extra" both players roll once

        if not extra == "extra": # If turn isn't the extra (players haven't drew)
            if rolls[0] == rolls[1]: # If both rolls are the same (double)
                print(f"{colour.cyan}You rolled a double!{colour.end}") # Scream in excitement
                rolls.append(self.roll()) # Add the roll to the rolls list, which is the bonus
                bonus = f"{colour.green}+{rolls[-1]}{colour.end} (rolled double)" # The bonus for the double

            elif sum(rolls) % 2:
                bonus = f"{colour.red}-5{colour.end} (odd score)" # The bonus for an odd total is -5
                rolls.append(-5) # Add the bonus to the end of the rolls list

            else:
                bonus = f"{colour.green}+10{colour.end} (even score)" # The bonus for an even total is +10
                rolls.append(10) # Add the bonus to the end of the rolls list

            time.sleep(1) # Wait one second
            print(f"Score: {colour.green}{rolls[0]} + {rolls[1]}{colour.end} = {colour.blue}{sum(rolls[0:2])}{colour.end}") # Show the score
            time.sleep(1) # Wait one second
            print(f"Bonus: {colour.green if rolls[-1] > 0 else colour.red}{bonus}{colour.end}") # Show the bonus
            time.sleep(1) # Wait one second
            print(
                f"Total: " +
                f"{colour.red}{score}{colour.end} " +
                f"{colour.green}+{sum(rolls[0:2])}{colour.end} " +
                f"{colour.green if rolls[-1] > 0 else colour.red}{'+' if rolls[-1] > 0 else ''}{rolls[-1]}{colour.end} " +
                f"= {colour.blue}{max(0, score + sum(rolls))}{colour.end}\n\n"
            ) # Print the total score, which also shows the math used to find it
        
        return sum(rolls)

    def round(self, round):
        print(f"{colour.magenta}Round {round+1}:{colour.end}") # Print the round number
        for player in self.playing.keys(): # Run for the amount of concurrent players
            self.playing[player] += self.turn(player, self.playing[player]) # The players score is the value returned by the turn() function
            self.playing[player] = max(0, self.playing[player]) # Set the players score to 0 if it becomes negative
            time.sleep(2) # Wait for 2 seconds

    def game_over(self):
        winner = {"username": max(self.playing, key=self.playing.get), "score": max(self.playing.values())} # Find the winner
        os.system("clear") # Clear the screen
        print(f"{colour.green}Game over! The winner is '{max(self.playing, key=self.playing.get)}'!{colour.end}\n") # Print the winner
        score_amount = 10 if self.num_players > 10 else self.num_players # Show a maximum of 10 scores on screen
        userdata.print_dict(f"Scores this game (Top {score_amount}):", self.playing, score_amount) # Print out the scores for this game

        data = userdata.read_data(self.data_file) # Read from the data file
        data["highscores"].append(winner) # Add the winner to the score history
        userdata.write_data(data, self.data_file) # Write to the data file

        userdata.print_dict("Highscores (Top 5):", {i["username"]: i["score"] for i in data["highscores"]}, 10) # Print out highscores

def user_manager():
    print(f"\n{colour.blue}User Manager:{colour.end}") # User Manager Title
    print(f"{colour.cyan}(C){colour.end}reate player, {colour.cyan}(D){colour.end}elete player, {colour.cyan}(E){colour.end}dit password, or {colour.cyan}(R){colour.end}eturn to menu:") # Menu options
    
    choice = input("> ").upper() # Ask for an input for the menu
    if choice == "C" or choice == "CREATE" or choice == "CREATE PLAYER": # Create player
        players.new_user(game.data_file) # Create player
        user_manager() # Run user_manager() again

    elif choice == "D" or choice == "DELETE" or choice == "DELETE PLAYER": # Delete player
        players.del_user(game.data_file) # Delete player
        user_manager() # Run user_manager() again

    elif choice == "E" or choice == "EDIT" or choice == "EDIT PASSWORD": # Edit password
        players.change_pass(game.data_file) # Change password
        user_manager() # Run user_manager() again

    elif choice == "R" or choice == "RETURN" or choice == "RETURN TO MENU": # Return to main menu
        print(f"{colour.red}Returning to main menu...{colour.end}\n") 
        # Don't run user_manager() again, menu() will run again once this ends

    else: 
        print(f"{colour.red}Error: Command not recognized{colour.end}\n") # Incorrect choice from the menu
        user_manager() # Run user_manager() again

game = Game() # Create a basic game object with default values

def menu():
    print(f"{colour.blue}Main Menu:{colour.end}") # Main menu title
    print(f"{colour.cyan}(S){colour.end}tart a game, {colour.cyan}(M){colour.end}anage players, {colour.cyan}(V){colour.end}iew highscores, or {colour.cyan}(E){colour.end}xit:") # Menu options
    choice = input("> ").upper() # Ask for an input for the menu

    if choice == "S" or choice == "START" or choice == "START A GAME": # Start the game
        print(f"{colour.blue}Configure the game before starting:{colour.end}") # Title
        num_players, rounds = configure.configure_game() # Configure the game

        game = Game(num_players=num_players, rounds=rounds) # Create a Game() object with the game settings

        for i in range(game.num_players): # Run for the amount of players
            game.playing = players.login_user(game.playing, game.data_file) # Login a user
        
        for i in [3,2,1]: # Countdown for 3 seconds
            print(f"{colour.magenta}The game will start in {i}... {colour.end}", end="\r") # Countdown will write over itself (\r)
            time.sleep(1) # Wait 1 second
        
        os.system("clear") # Clear the screen
        for round in range(game.rounds): # Run for the amount of rounds specified
            game.round(round) # Create a round, pass the round number

        while all(element == list(game.playing.values())[0] for element in game.playing.values()): # While all the players have the same score
            print(f"{colour.green}All players have the same score!{colour.end}") # Tell the players they have the same score
            time.sleep(1) # Wait 1 second
            os.system("clear") # Clear the screen
            print(f"\n{colour.magenta}Round: Sudden death{colour.end}") # Sudden death mode 
            for player in game.playing.keys(): # For the amount of players playing
                game.turn(player, game.playing[player], roll="extra") # Each player gets an extra turn

        game.game_over() # Game over
        menu() # Return to main menu

    elif choice == "M" or choice == "MANAGE" or choice == "MANAGE PLAYERS": # Manage players
        user_manager() # Manage players (recusrive functions)
        menu() # Return to main menu

    elif choice == "V" or choice == "VIEW" or choice == "VIEW HIGHSCORES": # View highscores
        os.system("clear") # Clear screen
        data = userdata.read_data(colour.data_file) # Read data from the data file
        userdata.print_dict("Highscores (Top 5):", {i["username"]: i["score"] for i in data["highscores"]}, 10) # Print the highscores
        menu() # Return to main menu

    elif choice == "E" or choice == "EXIT": # Exit the game
        print(f"{colour.red}Goodbye!{colour.end}") 
        # Say goodbye, and don't return to main menu

    else: # If command does not match any if statements
        print(f"{colour.red}Error: Command not recognized{colour.end}\n") # Command not recognized (not a choice in the menu)
        menu() # Return to main menu

# Start the game!!!
def main(): # Main function (Welcome)
    os.system("clear") # Clear the screen
    print(f"{colour.magenta}Welcome to Python Dice Game{colour.end} {colour.green}v2.1!{colour.end} {colour.red}{'(Development Mode Enabled)' if game.dev_mode == True else ''}{colour.end}") # Welcome message!
    menu() # Start the main menu

if __name__ == "__main__": # Only run if file is run directly with python. Do not run if included in another file.
    main() # Start the main function