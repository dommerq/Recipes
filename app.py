from flask import Flask
from flask_restful import Api
from daily import DailyRecipeSender, DailyRecipeReset

from resources.RecipeApi import RecipeResource, RecipesListResource


app = Flask(__name__)
api = Api(app)

api.add_resource(RecipeResource, '/recipe', '/recipe/<int:id>', endpoint="recipe")
api.add_resource(RecipesListResource, '/recipes', '/recipe/<int:id>', endpoint="recipes")
api.add_resource(DailyRecipeSender, '/daily', endpoint="daily")
api.add_resource(DailyRecipeReset, '/daily/reset', endpoint="dailyReset")

app.run(host='0.0.0.0', debug=True)