import colour as c

def player_amount():
    num_players = input(f"{c.cyan}How many players? (2 or more): {c.end}")
    
    if num_players.isnumeric() is False:
        print(f"{c.red}Error: Invalid input, not numeric{c.end}")
        player_amount()

    elif int(num_players) < 2:
        print(f"{c.red}Error: Amount of players is less than 2{c.end}")
        player_amount()

    else:
        return int(num_players)

def rounds_amount():
    rounds = input(f"{c.cyan}How many rounds (1 or more): {c.end}")

    if rounds.isnumeric() is False:
        print(f"{c.red}Error: Invalid input, not numeric{c.end}")
        rounds_amount()

    elif int(rounds) < 1:
        print(f"{c.red}Error: Amount of rounds is less than 1{c.end}")
        rounds_amount()
    
    else:
        return int(rounds)

def configure_game():
    num_players = player_amount()
    rounds = rounds_amount()

    return num_players, rounds