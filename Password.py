# imports for database
import requests
import pandas as pd
import sqlalchemy as db
# importing the API
from rdoclient import RandomOrgClient
# import used for validating URLs
import validators


# Returns a list of integers
def Valid_Password():
    # A password is valid if it contains at least one upper case letter,
    # one lower case letter, one number, and one special characters
    API_KEY = "1b4847da-504e-49b4-8256-797d1338de64"
    r = RandomOrgClient(API_KEY)
    random_ints = []
    random_ints.append(r.generate_integers(1, 65, 90))  # Upper case letter
    random_ints.append(r.generate_integers(1, 97, 122))  # Lower case letter
    random_ints.append(r.generate_integers(1, 48, 57))  # Number
    random_ints.append(r.generate_integers(1, 33, 47))  # Special character

    return random_ints


def Create_Password():
    valid_url = False
    while valid_url is not True:
        website = input(
            "What website is this password for?(Enter a valid URL) ")
        if validators.url(website):
            valid_url = True
        else:
            print("The URL you entered was invalid, try again.")

    # If the user already has this website in their database, ask if they want
    # to override the existing password
    select_query = db.select(password_table).where(
        password_table.c.website == website)
    result = connection.execute(select_query)

    # Check if the website exists in the database
    if result.fetchone():

        valid_input = False
        while valid_input is not True:
            user_input = input(
                f"The website '{website}' is already has a password. Would you like of override it?(Y/N) ")
            if user_input.lower() == "y":
                # Deletes the website from the database
                delete_query = db.delete(password_table).where(
                    password_table.c.website == website)
                result = connection.execute(delete_query)
                valid_input = True
            elif user_input.lower() == "n":
                valid_input = True
                return
            else:
                print("Your input was invalid, try again")

    API_KEY = "1b4847da-504e-49b4-8256-797d1338de64"
    # Makes sure the password has at least 10 characters

    valid_length = False
    length_value = 0

    while valid_length is not True:
        password_length = input(
            "How many characters should your password contain? ")

        if not password_length.isdigit():
            print("You must enter a valid integer, try again.")
            continue
        else:
            length_value = int(password_length)
        if length_value < 10:
            print("Your password must have at least 10 characters, try again.")
        else:
            valid_length = True

    r = RandomOrgClient(API_KEY)
    # Generates (PASSWORD_LENGTH - 4) random integers from 33 to 126
    random_ints = r.generate_integers(int(password_length) - 4, 33, 126)

    special_ints = Valid_Password()

    for num in special_ints:
        random_ints.append(num[0])

    password = ""

    for char in random_ints:
        password += chr(char)

    # Inserts the password into the database
    ins = password_table.insert().values(website=website, password=password)
    connection.execute(ins)

    print()
    print("PassWord: " + password)
    print()


def Quick_Create_Password():
    API_KEY = "1b4847da-504e-49b4-8256-797d1338de64"

    r = RandomOrgClient(API_KEY)
    # Quick generated password will be of size 20
    PASSWORD_LENGTH = 20

    # If the generated password is not valid, it keeps generating passwords
    # until one is

    # while valid_password is not True:
    random_ints = r.generate_integers(PASSWORD_LENGTH - 4, 33, 126)

    special_ints = Valid_Password()

    for num in special_ints:
        random_ints.append(num[0])

    password = ""

    for char in random_ints:
        password += chr(char)

    website = "No website, password was quick generated"

    # Inserts the password into the database
    ins = password_table.insert().values(website=website, password=password)
    connection.execute(ins)

    print()
    print("PassWord: " + password)
    print()


def Print_Password():
    # Retrieve and print the contents of the table
    select_query = db.select(password_table)
    result = connection.execute(select_query)

    print()
    print("Here are your passwords:")
    print()

    for row in result:
        print("Website:", row[0])
        print("Password:", row[1])
        print()


print()
print("Welcome to Password Generator!")
print()

data = {}
passwords = pd.DataFrame.from_dict(data)
engine = db.create_engine('sqlite:///passwords_data_base.db')
connection = engine.connect()

# Define the table schema
metadata = db.MetaData()
password_table = db.Table('password_table', metadata,
                          db.Column('website', db.String),
                          db.Column('password', db.String))

# Create the table
metadata.create_all(engine)

ask_user = True

while (ask_user):
    print("What would you like to do?")
    print("1) Generate New Password")
    print("2) Quick Generate Password")
    print("3) Show Passwords")
    print("4) Quit")
    user_input = input("(1/2/3/4) ")

    if user_input.strip() == "1":
        Create_Password()
    elif user_input.strip() == "2":
        Quick_Create_Password()
    elif user_input.strip() == "3":
        Print_Password()
    elif user_input.strip() == "4":
        ask_user = False
    else:
        print("Input is invalid, try again")

print()
print("Goodbye!")
print()
