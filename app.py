from flask import Flask
from flask_restful import Api

from resources.RecipeApi import RecipeResource, RecipesListResource


app = Flask(__name__)
api = Api(app)

api.add_resource(RecipeResource, '/recipe', '/recipe/<int:id>', endpoint="recipe")
api.add_resource(RecipesListResource, '/recipes', '/recipe/<int:id>', endpoint="recipes")

app.run(host='0.0.0.0', debug=True)