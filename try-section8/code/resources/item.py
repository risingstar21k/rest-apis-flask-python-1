import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from sqlalchemy import Integer
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )    

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {'message': f"An item with name '{name}' and already exists."}
        print("I AM EHRE")
        data = Item.parser.parse_args()      
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message":"An error occurred during inserting the item"}, 500
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()

        return{'message':'item has been deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        updated_item = ItemModel(name, data['price'], data['store_id'])

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, data['price'])

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [x.json() for x in ItemModel.query.all()]}
