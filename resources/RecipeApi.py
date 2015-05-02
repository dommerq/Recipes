from flask.ext.restful import reqparse, marshal
from flask_restful import Resource, abort, marshal_with, fields

from settings.db import session
from models.RecipeModel import Recipe

parser = reqparse.RequestParser()
parser.add_argument('id', type=int)
parser.add_argument('name', type=str)

recipe_fields = {
    'id': fields.Integer,
    'name': fields.String
}


class RecipeResource(Resource):

    @marshal_with(recipe_fields)
    def get(self, id):
        recipe = session.query(Recipe).filter(Recipe.id == id).first()
        if not recipe:
            abort(404, message="Recipe with id {} does not exist".format(id))
        return recipe, 201

    @marshal_with(recipe_fields)
    def put(self):
        args = parser.parse_args()
        recipe = session.query(Recipe).filter(Recipe.id == args['id']).first()
        if not recipe:
            recipe = Recipe()
        recipe.id = args['id']
        recipe.name = args['name']
        session.add(recipe)
        session.commit()
        return marshal(recipe, recipe_fields), 201


class RecipesListResource(Resource):

    @marshal_with(recipe_fields)
    def get(self):
        recipes = session.query(Recipe).all()
        return recipes