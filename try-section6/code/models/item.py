import sqlite3
from db import db

class ItemModel(db.Model):

    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))    

    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    def json(self):
        return {'name': self.name, 'price': self.price}
    
    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = f"SELECT * FROM items WHERE name = '{name}'"
        result = cursor.execute(query)
        row = result.fetchone()
        connection.close()
        if row:
            return cls(*row)

    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = f"INSERT INTO items values ('{self.name}',{self.price})"
        cursor.execute(query)
        connection.commit()
        connection.close()

    def update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = f"UPDATE items SET price = {self.price} WHERE name = '{self.name}'"
        cursor.execute(query)
        connection.commit()
        connection.close()