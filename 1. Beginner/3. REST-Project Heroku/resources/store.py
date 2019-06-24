from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        return store.json() if store else {'message': 'store not found'}, 404

    def post(self, name):

        if StoreModel.find_by_name(name):
            return {'message': 'store already exists'}

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {'message': 'error while creating the store'}, 500
        else:
            return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            store.delete_from_db()
            return {'message': 'Store Deleted'}
        else:
            return {'message': 'store does not exists'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
