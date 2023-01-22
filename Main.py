import argparse
from psycopg2 import connect, OperationalError
from Models import HOST, USER, PASSWORD, DATABASE, PORT, Message, Users

from clcrypto import check_password


def list_messages(cursor, username, password):
    user = Users.load_user_by_username(cursor, username)
    if not user:
        print('User does not exist')
    elif check_password(password, user.hashed_password):
        all_messages = Message.load_all_messages(cursor)
        for message in all_messages:
                print(message)
    else:
        print('Incorrect password')


def send_messages(cursor, username, password, to, message):
    user = Users.load_user_by_username(cursor, username)
    if not user:
        print('User does not exist')
    elif check_password(password, user.hashed_password):
        if len(message) > 255:
            print('Message is too long')

        message_to = Users.load_user_by_username(cursor, to)
        if message_to:
            message_from = Users.load_user_by_username(cursor, username)
            messages = Message(message_from.id, message_to.id, message)
            messages.save_to_db(cursor)
            print('Message sent')
        else:
            print('Recipent does not exist')


def main():
    try:
        cnx = connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, port=PORT)
        cnx.autocommit = True
        cursor = cnx.cursor()

        parser = argparse.ArgumentParser()
        parser.add_argument("-u", "--username", help="nazwa użytkownika")
        parser.add_argument("-p", "--password", help="hasło użytkownika")
        parser.add_argument("-t", "--to", help="nazwa użytkownika, do którego ma zostać wysłana wiadomość")
        parser.add_argument("-s", "--send", help="treść wiadomości")
        parser.add_argument("-l", "--list", help="listowanie wiadomości", action="store_true")

        args = parser.parse_args()

        if args.username and args.password and args.list:
            list_messages(cursor, args.username, args.password)

        elif args.username and args.password and args.to and args.send:
            send_messages(cursor, args.username, args.password, args.to, args.send)
        else:
            parser.print_help()

    except OperationalError:
        print('There was an error connecting to the server!')


if __name__ == '__main__':
    main()