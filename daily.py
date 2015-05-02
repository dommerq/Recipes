from flask import json
from flask.ext.restful import abort, Resource, marshal_with
from sqlalchemy import func
import requests
from resources.RecipeApi import recipe_fields

from settings.db import session
from models.RecipeModel import Recipe


headers = {
    "X-Parse-Application-Id": "SkwXEUQtF8aakn2cUYQi17yXXM0pB0xWT3AGrxiy",
    "X-Parse-REST-API-Key": "JMCstdhoTIV46FEzeeF9Z86lCrxecbRYX9nqBxLo",
    "Content-Type": "application/json"
}

parse_url = "https://api.parse.com/1/push"


class RandomRecipeFinder:

    def reset(self):
        for recipe in session.query(Recipe).all():
            recipe.done = False
        session.commit()

    def find(self):
        recipe = session.query(Recipe).filter(Recipe.done == False).order_by(func.random()).first()
        if not recipe:
            abort(500, message="Every recipe was done. Nice.")
        recipe.done = True
        session.commit()
        return recipe


class Parse:
    def sendPush(self, id):
        data = json.dumps({"data":{"recipe": "{}".format(id)}, "where":{}})
        r = requests.post(parse_url, headers=headers, data=data)
        print r.content


class DailyRecipeSender(Resource):

    @marshal_with(recipe_fields)
    def get(self):
        random = RandomRecipeFinder()
        # random.reset()
        id = random.find()

        parse = Parse()
        parse.sendPush(id)

        return id, 200


class DailyRecipeReset(Resource):
    def get(self):
        random = RandomRecipeFinder()
        random.reset()
        return "ok", 200

if __name__ == '__main__':
    random = RandomRecipeFinder()
    random.reset()
