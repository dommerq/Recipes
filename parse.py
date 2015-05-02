from flask import json
from sqlalchemy import func
import requests

from settings.db import session
from models.RecipeModel import Recipe


headers = {
    "X-Parse-Application-Id": "SkwXEUQtF8aakn2cUYQi17yXXM0pB0xWT3AGrxiy",
    "X-Parse-REST-API-Key": "JMCstdhoTIV46FEzeeF9Z86lCrxecbRYX9nqBxLo",
    "Content-Type": "application/json"
}

parse_url = "https://api.parse.com/1/push"

class RandomRecipeFinder:
    def find(self):
        recipe = session.query(Recipe).filter(Recipe.done == False).order_by(func.random()).first()
        return recipe.id

class Parse:
    def sendPush(self, id):
        data = json.dumps({"data":{"recipe": "{}".format(id)}, "where":{}})
        r = requests.post(parse_url, headers=headers, data=data)
        print r.content

if __name__ == '__main__':

    random = RandomRecipeFinder()
    id = random.find()

    parse = Parse()
    parse.sendPush(id)
