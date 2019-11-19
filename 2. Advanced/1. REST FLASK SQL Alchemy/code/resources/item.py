from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
)

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left black!")
    parser.add_argument('store_id', type=int, required=True, help="store id is required")

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'item not found'}, 404

    @fresh_jwt_required
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

    @jwt_required
    def delete(self, name):

        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'mesasge': 'admin user only'}, 401

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
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'items': items}, 200
        message = 'login to get more data' if items else None
        if message:
            return {'items': [item['name'] for item in items], 'message': message}, 200
        return {'items': []}
