# See LICENCE file for copyright and licence details

import colour
import hashlib
import getpass
import userdata

def get_username_and_pass(msg):
    print(f"\n{colour.blue}Enter a username and password to {msg}:{colour.end}")

    username = input("Username: ")
    password = hashlib.sha384(bytes(getpass.getpass("Password: "), "utf8")).hexdigest()

    return username, password

def del_user(data_file):
    username, password = get_username_and_pass("delete a user")
    data = userdata.read_data(data_file)
        
    if username not in data.keys():
        print(f"{colour.red}Error: User not found{colour.end}\n")

    elif data[username]["password"] != password:
        print(f"{colour.red}Error: Incorrect password{colour.end}\n")

    else:
        choice = input(f"{colour.red}Are you sure? (y/N): {colour.end}").upper()
        if choice == "Y" or choice == "YES":
            data.pop(username)
            userdata.write_data(data, data_file)
            print(f"{colour.green}User '{username}' successfully deleted.{colour.end}\n")

        else:
            print(f"{colour.red}Error: Operation cancelled.{colour.end}\n")

def new_user(data_file):
    username, password = get_username_and_pass("create a user")
    data = userdata.read_data(data_file)

    if username in data.keys():
        print(f"{colour.red}Error: Username taken{colour.end}\n")
        new_user(data_file)

    elif len(username) == 0:
        print(f"{colour.red}Error: Username cannot be empty{colour.end}\n")
        new_user(data_file)

    elif len(password) == 0:
        print(f"{colour.red}Error: Password cannot be empty{colour.end}\n")
        new_user(data_file)

    data[username] = { "password": password }
    userdata.write_data(data, data_file)

    print(f"{colour.green}User '{username}' successfully added.{colour.end}\n")

def edit_user(data_file):
    # TODO: edit a user
    # username, password = get_username_and_pass("edit a user")
    # data = userdata.read_data(data_file)

    # if username not in data.keys():
    #     print(f"{colour.red}Error: Username not found{colour.end}\n")
    #     edit_user(data_file)

    # elif data[username]["password"] != password:
    #     print(f"{colour.red}Error: Incorrect password{colour.end}")
    #     edit_user(data_file)
    
    # else:
    #     username, password = get_username_and_pass("to change your username and password.")
    print(f"{colour.red}Error: Editing a user coming soon{colour.end}")


def login_user(players, data_file):
    username, password = get_username_and_pass("login")
    data = userdata.read_data(data_file)

    if username in players.keys():
        print(f"{colour.red}Error: You're already in the game{colour.end}")
        login_user(players, data_file)

    elif username not in data.keys():
        print(f"{colour.red}Error: User not found{colour.end}")
        login_user(players, data_file)

    elif data[username]["password"] != password:
        print(f"{colour.red}Error: Incorrect password{colour.end}")
        login_user(players, data_file)

    else:
        players[username] = 0
        print(f"{colour.green}Success: Player '{username}' signed in{colour.end}")

    return players
