import argparse

from psycopg2 import OperationalError, connect

from Models import Users, HOST, USER, PASSWORD, DATABASE, PORT
from clcrypto import check_password

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="nazwa użytkownika")
parser.add_argument("-p", "--password", help="hasło użytkownika")
parser.add_argument("-n", "--new_password", help="nowe hasło")
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
        print('user deleted')
    else:
        print('Incorrect password')


def create_user(cursor, username, password):
    user = Users(username, password)
    all_users = Users.load_all_users(cursor)
    usernames = []
    for user_object in all_users:
        usernames.append(user_object.username)

    if username in usernames:
        print('This user already exists')

    else:
        if len(password) >= 8:
            user.save_to_db(cursor)
            print(f'User {username} created')
        else:
            print('Password is too short')


def edit_password(cursor, username, password, new_password):
    user = Users.load_user_by_username(cursor, username)
    if not user:
        print('User does not exist')
    else:
        if check_password(password, user.hashed_password):
            if len(new_password) >= 8:
                user.set_password(new_password)
                user.save_to_db(cursor)
                print(f'Password changed')
            else:
                print('Password is too short')

        else:
            print('Incorrect password')




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

        #message_1 = Message(8, 9, 'hello')
        #print(message_1)

        #message_1.save_to_db(cursor)

        if args.username and args.password and args.edit and args.new_password:
            edit_password(cursor, args.username, args.password, args.new_password)

        elif args.username and args.password:
            create_user(cursor, args.username, args.password)

        elif args.list:
            list_users(cursor)

        elif args.username and args.password and args.delete:
            delete_user(cursor, args.username, args.password)

        else:
            parser.print_help()

    except OperationalError:
        print('There was an error connecting to the server!')


if __name__ == '__main__':
    main()
