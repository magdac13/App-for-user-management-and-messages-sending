import argparse

from psycopg2 import OperationalError, connect

from Models import Users, Message, HOST, USER, PASSWORD, DATABASE, PORT
from clcrypto import check_password

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="nazwa użytkownika")
parser.add_argument("-p", "--password", help="hasło użytkownika")
parser.add_argument("-n", "--new_pass", help="nowe hasło")
parser.add_argument("-l", "--list", help="listowanie użytkowników", action="store_true")
parser.add_argument("-d", "--delete", help="usuwanie użytkownika", action="store_true")
parser.add_argument("-e", "--edit", help="edycja użytkownika", action="store_true")

args = parser.parse_args()


def list_users(cursor):
    all_users = Users.load_all_users(cursor)
    for user in all_users:
        print(user.username)


def delete_user(cursor, username, password):
    user = Users.load_user_by_username(cursor, username)
    if not user:
        print('User does not exist')
    elif check_password(password, user.hashed_password):
        user.delete(cursor)
        print(user.delete(cursor), 'user deleted')
    else:
        print('Incorrect password')


def create_user(cursor, username, password):
    user = Users(username, password)
    all_users = Users.load_all_users(cursor)
    if user in all_users:
        print('This user already exists')

    else:
        if len(password) >= 8:
            user.save_to_db(cursor)
        else:
            print('Password is too short')


def main():
    try:
        cnx = connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, port=PORT)
        cnx.autocommit = True
        cursor = cnx.cursor()

        user_1 = Users('Magda', 'password_1')
        #user_1.save_to_db(cursor)

        user_2 = Users('Michał', 'password_2')
        #user_2.save_to_db(cursor)

        #user_3 = Users('Kacper', 'password_3')
        #user_3.save_to_db(cursor)

        #u = user_1.load_user_by_username(cursor, 'Magda')
        #print(u)

        #u = user_1.load_all_users(cursor)
        #print(u)
        #u.delete(cursor)

        message_1 = Message(8, 9, 'hello')
        print(message_1)

        #message_1.save_to_db(cursor)

    except OperationalError:
        print('There was an error connecting to the server!')


    if args.list:
        list_users(cursor)


    elif args.delete:
        # usuwanie użytkowników
        pass
    elif args.edit:
        # edycja użytkownika
        pass
    else:
        # logowanie
        pass

    if args.username and args.password:
        # sprawdzanie nazwy użytkownika i hasła
        pass
    elif args.username and args.new_pass:
        # zmiana hasła
        pass
    else:
        parser.print_help()


if __name__ == '__main__':
    main()