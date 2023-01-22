from clcrypto import hash_password
from psycopg2 import connect, OperationalError


HOST = 'localhost'
USER = 'postgres'
PASSWORD = 'coderslab'
DATABASE = 'test_db'
PORT = 3333


class Users:
    def __init__(self, username="", password="", salt=""):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=""):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def save_to_db(self, cursor):

        if self._id == -1:
            sql = """INSERT INTO users(username, hashed_password)
                            VALUES(%s, %s) RETURNING id"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE Users SET username = %s, hashed_password  = %s
                           WHERE id=%s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_username(cursor, username):
        sql = "SELECT id, username, hashed_password FROM users WHERE username=%s"
        cursor.execute(sql, (username,))  # (username) - cause we need a tuple
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = Users(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user

    @staticmethod
    def load_user_by_id(cursor, id_):
        sql = "SELECT id, username, hashed_password FROM users WHERE id=%s"
        cursor.execute(sql, (id_,))  # (id_, ) - cause we need a tuple
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = Users(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, hashed_password FROM Users"
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = Users()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete(self, cursor):
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (self.id,))
        self._id = -1
        return True

    def __str__(self):
        user_info = f'{self.username} has id of {self._id} and their hashed password is {self._hashed_password}'
        return user_info


class Message:
    def __init__(self, from_id='', to_id='', text=''):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self._creation_date = None

    def __str__(self):
        message_info = f'Message from user ID {self.from_id} to user ID {self.to_id} is: {self.text} '
        return message_info

    @property
    def id(self):
        return self._id

    @property
    def creation_date(self):
        return self._creation_date

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO Messages(from_id, to_id, text)
                            VALUES(%s, %s, %s) RETURNING id, creation_date"""
            values = (self.from_id, self.to_id, self.text)
            cursor.execute(sql, values)
            self._id, self._creation_date = cursor.fetchone()
            return True
        else:
            sql = """UPDATE Messages SET to_id = %s, from_id = %s, text = %s WHERE id=%s"""
            values = (self.from_id, self.to_id, self.text, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_all_messages(cursor):
        sql = "SELECT id, from_id, to_id, creation_date, text FROM Messages"
        messages = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, from_id, to_id, creation_date, text = row
            load_message = Message()
            load_message._id = id_
            load_message.from_id = from_id
            load_message.to_id = to_id
            load_message._creation_date = creation_date
            load_message.text = text
            messages.append(load_message)
        return messages


def main():
    try:
        cnx = connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, port=PORT)
        cnx.autocommit = True
        cursor = cnx.cursor()

        user_1 = Users('Magda', 'password_1')
        #user_1.save_to_db(cursor)

        user_2 = Users('Michał', 'password_2')
        #user_2.save_to_db(cursor)

        #user_3 = Users('Kasia', 'password_4')
        #user_3.save_to_db(cursor)

        #u = user_1.load_user_by_username(cursor, 'Magda')
        #print(u)

        #u = user_1.load_all_users(cursor)
        #print(u)
        #u.delete(cursor)

        #message_1 = Message(8, 9, 'hello')
        #print(message_1)

        #message_2 = Message(9, 8, 'hello')
        #message_2.save_to_db(cursor)

        #message_3 = Message(8, 16, 'hello')
        #message_3.save_to_db(cursor)

        #message_1.save_to_db(cursor)

    except OperationalError:
        print('There was an error connecting to the server!')


if __name__ == '__main__':
    main()



