from flask import json
from flask.ext.restful import reqparse

from flask_restful import Resource, abort, marshal_with, fields

from schema.schema import recipe_schema

from settings.db import session
from models.RecipeModel import Recipe


parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('name', type=str)

recipe_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'image_url': fields.String,
    'primary_ingredient': fields.String,
    'rating': fields.Float,
    'yielding_number': fields.Integer,
    'yielding_unit': fields.String
}

bigoven_url = "http://api.bigoven.com/recipe/"
bigoven_api_key = "dvx2ltBtHBdWhm089ckN77qkpZ3lNjp1"


def get_recipe_from_bigoven():
    # headers = {'Content-type': 'application/json'}
    # r = requests.get(bigoven_url + str(args['id']) + "?api_key=" + bigoven_api_key, headers=headers)
    # return r.content
    with open('recipe.json', 'r') as content_file:
        content = content_file.read()
    return content


class RecipeResource(Resource):

    @marshal_with(recipe_fields)
    def get(self, id):
        recipe = session.query(Recipe).filter(Recipe.id == id).first()
        if not recipe:
            abort(404, message="Recipe with id {} does not exist".format(id))
        return recipe, 201

    def put(self):
        args = parser.parse_args()
        recipeJson = get_recipe_from_bigoven()
        recipe, err = recipe_schema.load(json.loads(recipeJson))

        # recipe = session.query(Recipe).filter(Recipe.id == args['id']).first()
        # if not recipe:
        #     recipe = Recipe()
        # recipe.id = args['id']
        # recipe.name = args['name']
        session.add(recipe)
        session.commit()
        return recipe_schema.dump(recipe), 201


class RecipesListResource(Resource):

    @marshal_with(recipe_fields)
    def get(self):
        recipes = session.query(Recipe).all()
        return recipes