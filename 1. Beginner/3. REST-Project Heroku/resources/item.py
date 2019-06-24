from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left black!")
    parser.add_argument('store_id', type=int, required=True, help="store id is required")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'item {} already exists'.format(name)}, 400  # Something did go wrong with the server

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)
        # item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500  # Internal server error
        else:
            return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()
            return {'message': 'item deleted'}
        else:
            {'mesasge': 'item not found'}, 404

    def put(self, name):

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        try:
            if item:
                item.price = data['price']
                item.store_id = data['store_id']
            else:
                item = ItemModel(name, **data)
                # item = ItemModel(name, data['price'], data['store_id'])
            item.save_to_db()
            return item.json()
        except:
            return {'message': 'error while updating an item.'}, 500


class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda item: item.json(), ItemModel.query.all()))}
