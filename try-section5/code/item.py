import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = f"SELECT * FROM items WHERE name = '{name}'"
        result = cursor.execute(query)
        row = result.fetchone()
        connection.close()
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}


    def post(self, name):
        if self.find_by_name(name):
            return {'message': f"An item with name '{name}' already exists."}

        data = Item.parser.parse_args()      
        item = {'name': name, 'price': data['price']}

        try:
            self.insert(item)
        except:
            return {"message":"An error occurred during inserting the item"}, 500
        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = f"INSERT INTO items values ('{item['name']}',{item['price']})"
        cursor.execute(query)
        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = f"UPDATE items SET price = {item['price']} WHERE name = '{item['name']}'"
        cursor.execute(query)
        connection.commit()
        connection.close()

    @jwt_required()
    def delete(self, name):
        global items
        if self.find_by_name(name):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = f"DELETE FROM items WHERE name = '{name}'"
            cursor.execute(query)
            connection.commit()
            connection.close()   
            return {'message': f'Item: {name} deleted'}, 201
        return {'message': f"An item with name '{name}' not found."}   
        

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        updated_item = {'name': name, 'price': data['price']}

        if self.find_by_name(name):
            try:
                self.update(updated_item)
            except:
                return {"message": "An error occurred while updating the item"}, 500
        else:
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error occurred while inserting the item"}, 500
        return updated_item

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = f"SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        connection.close()
        return {'items': items}
