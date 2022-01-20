# See LICENCE file for copyright and licence details
# Github: https://github.com/SpyHoodle/python-dice-game

# Import needed libraries
import colour as c
import hashlib
import getpass
import userdata


def get_pass():
    # Ask for a password, whilst hiding what the user types
    input_password = getpass.getpass("Password: ")
    # Return a sha384 hashed version of the password
    return hashlib.sha384(bytes(input_password,"utf8")).hexdigest()


def get_username_and_pass(msg):
    # Print out the message
    print(f"\n{c.blue}Enter a username and password to {msg}:{c.end}")

    # Ask for a username
    username = input("Username: ").upper()
    # Ask for a password
    password = get_pass()

    # Return the username and password
    return username, password


def del_user(data_file):
    # Ask for a username and password for which user to delete
    username, password = get_username_and_pass("delete a user")
    # Read from the data file
    data = userdata.read_data(data_file)

    # If the username isn't found
    if username not in data.keys():
        # Tell the user that the user isn't found
        print(f"{c.red}Error: User not found{c.end}")
        # Ask again
        del_user(data_file)

    # If the hashed password does not match the username's hashed password
    elif data[username]["password"] != password:
        # Tell the user that the password is incorrect
        print(f"{c.red}Error: Incorrect password{c.end}")
        # Ask again
        del_user(data_file)

    # The username and password must be correct
    else:
        # Ask the user to confirm if they are sure
        choice = input(f"{c.red}Are you sure? (y/N): {c.end}").upper()
        # If the user says yes
        if choice == "Y" or choice == "YES":
            # Delete the user from the dictionary
            data.pop(username)
            # Write the dictionary to the data file
            userdata.write_data(data, data_file)
            # Tell the user it was a success
            print(f"{c.green}User '{username}' successfully deleted.{c.end}")

        # If the user types anything but yes
        else:
            # Tell them
            print(f"{c.red}Error: Operation cancelled.{c.end}")


def new_user(data_file):
    # Ask for a username and password to create a user
    username, password = get_username_and_pass("create a user")
    # Read from the data file
    data = userdata.read_data(data_file)

    # If username already exists
    if username in data.keys():
        # Tell the user that the username is taken
        print(f"{c.red}Error: Username taken{c.end}")
        # Ask again
        new_user(data_file)

    # If username has no length (no characters)
    elif len(username) == 0:
        # Tell the user their username has to have characters
        print(f"{c.red}Error: Username cannot be empty{c.end}")
        # Ask again
        new_user(data_file)

    # If password has no length (no characters)
    elif len(password) == 0:
        # Tell the user theur password has to have characters
        print(f"{c.red}Error: Password cannot be empty{c.end}")
        # Ask again
        new_user(data_file)

    else:
        # Create a username with the "password" of the hashed password
        data[username] = {"password": password}
        # Write the data to the data file
        userdata.write_data(data, data_file)

        # Tell the user we successfully added their user
        print(f"{c.green}User '{username}' successfully added.{c.end}")


def change_pass(data_file):
    # Ask for a username and password to login and change their password
    username, password = get_username_and_pass("login and change your password")
    # Read from the data file
    data = userdata.read_data(data_file)

    # If the username isn't found
    if username not in data.keys():
        # Tell the user we couldn't find their username
        print(f"{c.red}Error: Username not found{c.end}")
        # Ask again
        change_pass(data_file)

    # If the password is incorrect
    elif data[username]["password"] != password:
        # Tell the user the password is incorrect
        print(f"{c.red}Error: Incorrect password{c.end}")
        # Ask again
        change_pass(data_file)

    # The username and password must be correct
    else:
        # Ask for a new password
        print(f"\n{c.blue}Enter your new password:{c.end}")
        # Don't show what the user types in
        password = get_pass()

        # Change username's password to the new password
        data[username] = {"password": password}
        # Write to the data file
        userdata.write_data(data, data_file)

        # Tell the user that we succeeded in changing their password
        print(f"{c.green}Password for user '{username}' successfully changed{c.end}")


def login_user(players, data_file):
    # Ask for a username and password to login
    username, password = get_username_and_pass("login")
    # Read from the data file
    data = userdata.read_data(data_file)

    # If the user has already logged in
    if username in players.keys():
        # Tell the user they're already in the game
        print(f"{c.red}Error: You're already in the game{c.end}")
        # Ask again
        login_user(players, data_file)

    # If username isn't found
    elif username not in data.keys():
        # Tell the user that their username isn't found
        print(f"{c.red}Error: User not found{c.end}")
        # Ask again
        login_user(players, data_file)

    # If the password is incorrect
    elif data[username]["password"] != password:
        # Tell the user that their password is incorrect
        print(f"{c.red}Error: Incorrect password{c.end}")
        login_user(players, data_file)

    # Username and password must be correct
    else:
        # Create a new player in players - with 0 score
        players[username] = 0
        # Tell the user that they have succesfully signed in
        print(f"{c.green}Success: Player '{username}' signed in{c.end}")

    # Return the players
    return players
