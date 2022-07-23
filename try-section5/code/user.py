import sqlite3
import string
from flask_restful import Resource, reqparse

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor();

        query = f"SELECT * FROM users WHERE username = '{username}'"

        result = cursor.execute(query)
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None
        
        connection.close()
        return user
    
    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor();

        query = f"SELECT * FROM users WHERE id = {_id}"

        result = cursor.execute(query)
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None
        
        connection.close()
        return user


class UserRegister(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": f"{data['username']} user already exists"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor();

        query = f"INSERT INTO users VALUES (NULL, '{data['username']}', '{data['password']}')"
        cursor.execute(query)

        connection.commit()
        connection.close()

        return{"message": f"User {data['username']} created successfully"}, 201
