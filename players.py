# See LICENCE file for copyright and licence details

import colour
import hashlib
import getpass
import userdata


def get_pass():
    input_password = getpass.getpass("Password: ")
    return hashlib.sha384(bytes(input_password,"utf8")).hexdigest()


def get_username_and_pass(msg):
    print(f"\n{colour.blue}Enter a username and password to {msg}:{colour.end}")

    username = input("Username: ")
    password = get_pass()

    return username, password


def del_user(data_file):
    username, password = get_username_and_pass("delete a user")
    data = userdata.read_data(data_file)

    if username not in data.keys():
        print(f"{colour.red}Error: User not found{colour.end}")
        del_user(data_file)

    elif data[username]["password"] != password:
        print(f"{colour.red}Error: Incorrect password{colour.end}")

    else:
        choice = input(
            f"{colour.red}Are you sure? (y/N): {colour.end}").upper()
        if choice == "Y" or choice == "YES":
            data.pop(username)
            userdata.write_data(data, data_file)
            print(f"{colour.green}User '{username}' successfully deleted.{colour.end}")

        else:
            print(f"{colour.red}Error: Operation cancelled.{colour.end}")


def new_user(data_file):
    username, password = get_username_and_pass("create a user")
    data = userdata.read_data(data_file)

    if username in data.keys():
        print(f"{colour.red}Error: Username taken{colour.end}")
        new_user(data_file)

    elif len(username) == 0:
        print(f"{colour.red}Error: Username cannot be empty{colour.end}")
        new_user(data_file)

    elif len(password) == 0:
        print(f"{colour.red}Error: Password cannot be empty{colour.end}")
        new_user(data_file)

    else:
        data[username] = { "password": password }
        userdata.write_data(data, data_file)

        print(f"{colour.green}User '{username}' successfully added.{colour.end}")


def change_pass(data_file):
    username, password = get_username_and_pass("login and change your password")
    data = userdata.read_data(data_file)

    if username not in data.keys():
        print(f"{colour.red}Error: Username not found{colour.end}")
        change_pass(data_file)

    elif data[username]["password"] != password:
        print(f"{colour.red}Error: Incorrect password{colour.end}")
        change_pass(data_file)

    else:
        print(f"\n{colour.blue}Enter your new password:{colour.end}")
        password = get_pass()

        data[username] = {"password": password}
        userdata.write_data(data, data_file)

        print(f"{colour.green}Password for user '{username}' successfully changed{colour.end}")


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
