from marshmallow import Schema

from models.RecipeModel import Recipe, Ingredient


class RecipeSchema(Schema):

    class Meta:
        fields = ('RecipeID', 'Title', 'ImageURL', "PrimaryIngredient", "StarRating", "YieldNumber", "YieldUnit", "Ingredients")

    def make_object(self, data):
        recipe = Recipe()
        recipe.id = data.get('RecipeID')
        recipe.title = data.get('Title')
        recipe.image_url = data.get('ImageURL')
        recipe.primary_ingredient = data.get('PrimaryIngredient')
        recipe.rating = data.get('StarRating')
        recipe.yielding_number = data.get('YieldNumber')
        recipe.yielding_unit = data.get('YieldUnit')

        for ingredient in data.get('Ingredients'):
            ing = ingredient_schema.make_object(ingredient)
            recipe.ingredients.append(ing)

        return recipe


class IngredientSchema(Schema):
    class Meta:
        fields = ('IngredientId', 'Name', 'MetricDisplayQuantity', "MetricUnit", "PreparationNotes")

    def make_object(self, data):
        ingredient = Ingredient()
        ingredient.id = data.get('IngredientID')
        ingredient.name = data.get('Name')
        ingredient.metric_display_quantity = data.get('MetricDisplayQuantity')
        ingredient.metric_unit= data.get('MetricUnit')
        ingredient.preparation_notes = data.get('PreparationNotes')
        return ingredient


recipe_schema = RecipeSchema()
ingredient_schema = IngredientSchema()
