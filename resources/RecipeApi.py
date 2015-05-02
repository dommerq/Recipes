from flask import json
from flask.ext.restful import reqparse

from flask_restful import Resource, abort, marshal_with, fields
import requests
from sqlalchemy import and_

from schema.schema import recipe_schema

from settings.db import session
from models.RecipeModel import Recipe


parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('name', type=str)

ingredient_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'quantity': fields.String(attribute="metric_display_quantity"),
    'unit': fields.String(attribute="metric_unit"),
    'preparation': fields.String(attribute="preparation_notes")
}

recipe_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'image_url': fields.String,
    'primary_ingredient': fields.String,
    'rating': fields.Float,
    'instructions': fields.String,
    'done': fields.Boolean,
    'url': fields.String,
    'yielding_number': fields.Integer,
    'yielding_unit': fields.String,
    'ingredients': fields.List(fields.Nested(ingredient_fields))
}

bigoven_url = "http://api.bigoven.com/recipe/"
bigoven_api_key = "dvx2ltBtHBdWhm089ckN77qkpZ3lNjp1"


def get_recipe_from_bigoven(id):
    headers = {'Content-type': 'application/json'}
    r = requests.get(bigoven_url + str(id) + "?api_key=" + bigoven_api_key, headers=headers)
    print r.content
    return r.content
    # with open('recipe.json', 'r') as content_file:
    #     content = content_file.read()
    # return content

class RecipeResource(Resource):

    @marshal_with(recipe_fields)
    def get(self, id):
        recipe = session.query(Recipe).filter(and_(Recipe.id == id), (Recipe.done == False)).first()

        if not recipe:
            abort(404, message="Recipe with id {} does not exist or has already been done".format(id))
        session.commit()
        return recipe, 201

    @marshal_with(recipe_fields)
    def put(self):
        args = parser.parse_args()
        recipeJson = get_recipe_from_bigoven(args["id"])
        recipe, err = recipe_schema.load(json.loads(recipeJson))
        session.add(recipe)
        session.commit()
        return recipe, 201


class RecipesListResource(Resource):

    @marshal_with(recipe_fields)
    def get(self):
        recipes = session.query(Recipe).all()
        return recipes