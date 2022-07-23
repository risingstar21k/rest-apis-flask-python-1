import sqlite3
import string
from flask_restful import Resource, reqparse
from models.user import UserModel



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

        if UserModel.find_by_username(data['username']):
            return {"message": f"{data['username']} user already exists"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor();

        query = f"INSERT INTO users VALUES (NULL, '{data['username']}', '{data['password']}')"
        cursor.execute(query)

        connection.commit()
        connection.close()

        return{"message": f"User {data['username']} created successfully"}, 201
