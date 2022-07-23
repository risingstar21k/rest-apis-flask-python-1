from crypt import methods
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

stores = [
    {
        "name":"My wonderful Store",
        "items":[
            {
                "name":"myItem",
                "price":15.99
            }
        ]
    }
]

print(stores)

@app.route('/')
def home():
     return render_template('index.html')

# POST /store data(name)
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        "name":request_data['name'],
        "items":[]
    }

    stores.append(new_store)
    return jsonify(new_store)

# Get /store/<string name>
@app.route('/store/<string:name>')
def get_store(name):
    # iterate over stores
    # if the store name matches, return it, else return an error message

    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({"message":"store not found"})

# GET /store
@app.route('/store')
def get_stores():
    return jsonify({"stores": stores})

# POST /store/<string:name>/item
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({"message":"store not found"})

# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({"items": store['items']})
    return jsonify({"message":"store not found"})



app.run()