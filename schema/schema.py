from marshmallow import Schema, fields
from models.RecipeModel import Recipe


class RecipeSchema(Schema):

    class Meta:
        fields = ('RecipeID', 'Title', 'ImageURL', "PrimaryIngredient", "StarRating", "YieldNumber", "YieldUnit")

    def make_object(self, data):
        recipe = Recipe()
        recipe.id = data.get('RecipeID')
        recipe.title = data.get('Title')
        recipe.image_url = data.get('ImageURL')
        recipe.primary_ingredient = data.get('PrimaryIngredient')
        recipe.rating = data.get('StarRating')
        recipe.yielding_number = data.get('YieldNumber')
        recipe.yielding_unit = data.get('YieldUnit')
        return recipe


class IngredientSchema(Schema):
    pass

recipe_schema = RecipeSchema()
# ingredient_schema = IngredientSchema()
