"""
the server then Sees GET / HTTP/1.1
GET -> Verb
/ -> Path
HTTP/1.1 -> Protocol

example:
    GET /login HTTP/1.1
    Host: https://twitter.com/login

GET: used to send data back only (normally returns HTML or text or errors)
POST: used to receive data
PUT: Make sure something is there
DELETE: Remove something
"""


from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
stores = \
    [
        {
            "name": "My First Store",
            "items":
                [
                    {
                        "name": "My Item",
                        "price": 9.99
                    }
                ]
        }
    ]


@app.route('/')  # 'http://www.google.com/'
def home():
    return render_template('index.html')


@app.route('/store')
# GET /store
def get_stores():
    return jsonify({'stores': stores})


@app.route('/store/<string:name>')  # 'http://localhost:5000/some_name'
# GET /store/<string:name>
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'store not found'})


@app.route('/store/<string:name>/item')
# GET /store/<string:name>/item
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'store not found'})


@app.route('/store', methods=['POST'])
# POST /store data: {name:}
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


@app.route('/store/<string:name>/item', methods=['POST'])
# POST /store/<string:name>/item {name:, price:}
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
    return jsonify({'message': 'store not found'})


app.run(port=5000, debug=True)
