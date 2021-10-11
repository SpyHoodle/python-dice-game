# See LICENCE file for copyright and licence details

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

import random
import time
import os
import colour
import userdata
import players

class Game:
    def __init__(self, **kwargs):
        self.dev_mode = True
        self.num_players = 2
        self.rounds = 3
        self.data_file = "data.json"
        self.playing = {}

        for k, v in kwargs.items():
            setattr(self, k, v)

    def roll(self):
        input(f"{colour.green}Press enter to roll{colour.end}")

        print("Rolling...", end="\r")
        time.sleep(0.5)
        roll = random.randint(1, 6)

        print(f"You rolled a: {roll}\n")
        return roll

    def turn(self, player, score, extra=None):
        print(f"{colour.blue}Player: {player}{colour.end}")
        print(f"{colour.blue}Score: {game.playing[player]}{colour.end}\n")
        rolls = [self.roll() for _ in range(1 if extra == "extra" else 2)]

        if not extra == "extra":
            if rolls[0] == rolls[1]:
                print(f"{colour.cyan}You rolled a double!{colour.end}")
                rolls.append(self.roll())
                bonus = f"{colour.green}+{rolls[-1]}{colour.end} (rolled double)"

            elif sum(rolls) % 2:
                bonus = f"{colour.red}-5{colour.end} (odd score)"
                rolls.append(-5)

            else:
                bonus = f"{colour.green}+10{colour.end} (even score)"
                rolls.append(10)

            time.sleep(1)
            print(f"Score: {colour.green}{rolls[0]} + {rolls[1]}{colour.end} = {colour.blue}{sum(rolls[0:2])}{colour.end}")
            time.sleep(1)
            print(f"Bonus: {colour.green if rolls[-1] > 0 else colour.red}{bonus}{colour.end}")
            time.sleep(1)
            print(
                f"Total: " +
                f"{colour.red}{score}{colour.end} " +
                f"{colour.green}+{sum(rolls[0:2])}{colour.end} " +
                f"{colour.green if rolls[-1] > 0 else colour.red}{'+' if rolls[-1] > 0 else ''}{rolls[-1]}{colour.end} " +
                f"= {colour.blue}{max(0, score + sum(rolls))}{colour.end}\n\n"
            )
        
        return sum(rolls)

    def round(self, round):
        print(f"{colour.magenta}Round {round+1}:{colour.end}")
        for player in game.playing.keys():
            self.playing[player] += self.turn(player, self.playing[player])
            self.playing[player] = max(0, self.playing[player])
            time.sleep(2)

    def game_over(self):
        winner = {"username": max(game.playing, key=game.playing.get), "score": max(game.playing.values())}
        os.system("clear")
        print(f"{colour.green}Game over! The winner is '{max(game.playing, key=game.playing.get)}'!{colour.end}\n")
        score_amount = 10 if game.num_players > 10 else game.num_players
        userdata.print_dict(f"Scores this game (Top {score_amount}):", game.playing, score_amount)

        data = userdata.read_data(game.data_file)
        data["highscores"].append(winner)
        userdata.write_data(data, game.data_file)

        userdata.print_dict("Highscores (Top 5):", {i["username"]: i["score"] for i in data["highscores"]}, 10)

def user_manager():
    print(f"\n{colour.blue}User Manager:{colour.end}")
    print(f"{colour.cyan}(C){colour.end}reate player, {colour.cyan}(D){colour.end}elete player, {colour.cyan}(E){colour.end}dit player, or {colour.cyan}(R){colour.end}eturn to menu:")
    
    choice = input("> ").upper()
    if choice == "C" or choice == "CREATE" or choice == "CREATE PLAYER":
        players.new_user(game.data_file)
        user_manager()

    elif choice == "D" or choice == "DELETE" or choice == "DELETE  PLAYER":
        players.del_user(game.data_file)
        user_manager()

    elif choice == "E" or choice == "EDIT" or choice == "EDIT PLAYER":
        players.edit_user(game.data_file)
        user_manager()

    elif choice == "R" or choice == "RETURN" or choice == "RETURN TO MENU":
        print(f"{colour.red}Returning to main menu...{colour.end}\n")

    else:
        print(f"{colour.red}Error: Command not recognized{colour.end}\n")
        user_manager()

game = Game()

def menu():
    print(f"{colour.blue}Main Menu:{colour.end}")
    print(f"{colour.cyan}(S){colour.end}tart a game, {colour.cyan}(M){colour.end}anage players, {colour.cyan}(V){colour.end}iew highscores, or {colour.cyan}(E){colour.end}xit:")
    choice = input("> ").upper()

    if choice == "S" or choice == "START" or choice == "START A GAME":
        for i in range(game.num_players):
            game.playing = players.login_user(game.playing, game.data_file)
        
        for i in range(1,4):
            print(f"{colour.magenta}The game will start in {i}... {colour.end}", end="\r")
            time.sleep(1)
        
        os.system("clear")
        for round in range(game.rounds):
            game.round(round)

        while all(element == list(game.playing.values())[0] for element in game.playing.values()):
            print(f"{colour.green}All players have the same score!{colour.end}")
            time.sleep(1)
            os.system("clear")
            print(f"\n{colour.magenta}Round: Sudden death{colour.end}")
            for player in game.playing.keys():
                game.turn(player, game.playing[player], roll="extra")

        game.game_over()
        menu()

    elif choice == "M" or choice == "MANAGE" or choice == "MANAGE PLAYERS":
        user_manager()   
        menu()
        

    elif choice == "V" or choice == "VIEW" or choice == "VIEW HIGHSCORES":
        os.system("clear")
        data = userdata.read_data(game.data_file)
        userdata.print_dict("Highscores (Top 5):", {i["username"]: i["score"] for i in data["highscores"]}, 10)
        menu()

    elif choice == "E" or choice == "EXIT":
        print(f"{colour.red}Goodbye!{colour.end}")

    else:
        print(f"{colour.red}Error: Command not recognized{colour.end}\n")
        menu()

# Start the game!!!
def main():
    os.system("clear")
    print(f"{colour.magenta}Welcome to Python Dice Game{colour.end} {colour.green}v2.1!{colour.end} {colour.red}{'(Development Mode Enabled)' if game.dev_mode == True else ''}{colour.end}")
    menu()

if __name__ == "__main__":
    main()