"""App api"""
from flask_restful import Resource, marshal_with, reqparse
from DoList import db
from .serializers import ItemListSchema
from ..models import Item
from flask import request, jsonify


class ItemsResource(Resource):
    @marshal_with(ItemListSchema)
    def get(self):
        """get"""
        try:
            return Item.query.all()
        except Exception:
            return {'message': "Getting exception."}, 500

    def delete(self):
        """del"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('item_id')
            parser = parser.parse_args()
            item_id = parser['item_id']
            item = Item.query.filter(Item.id == item_id).first()

            db.session.delete(item)
            db.session.commit()
            return {'message': "Item deleted."}, 204
        except Exception:
            return {'message': "Deleting exception."}, 500

    @marshal_with(ItemListSchema)
    def post(self, *args):
        """post"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('title')
            parser.add_argument('text')
            parser.add_argument('slug')
            parser.add_argument('is_completed')
            parser = parser.parse_args()
            title = parser['title']
            text = parser['text']
            slug = parser['slug']
            is_completed = bool(parser['is_completed'])
            item = Item(title, text, slug, is_completed)

            db.session.add(item)
            db.session.commit()
            return {'message': "Posted"}, 201
        except Exception:
            return {'message': "Add exception."}, 500

    # @marshal_with(ItemListSchema)
    def put(self):
        """put"""
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('item_id')
            parser.add_argument('title')
            parser.add_argument('text')
            parser.add_argument('slug')
            parser.add_argument('is_completed')
            parser = parser.parse_args()
            item_id = parser['item_id']
            item = Item.query.filter(Item.id == int(item_id)).first()
            item.title = parser['title']
            item.text = parser['text']
            item.slug = parser['slug']
            item.is_completed = bool(parser['is_completed'])

            db.session.commit()
            db.session.close()
            return {'message': "Putted"}, 202
        except Exception:
            return {'message': "Put exception."}, 500
