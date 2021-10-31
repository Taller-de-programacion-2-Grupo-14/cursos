from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.recipe import Recipe, recipe_list

# Si o si tiene que heredar de Resource sino pasan cosas raras, en el put el request lo recibe de alguna forma misteriosa y magica
class RecipeResource(Resource):

    def __init__(self, sarasa):
        self.sarasa = sarasa

    def get(self, recipe_id):
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id and recipe.is_publish),None)

        if recipe is None:
            return {'message': self.sarasa}, HTTPStatus.NOT_FOUND

        return recipe.data, HTTPStatus.OK
    
    def put(self, recipe_id):
        data = request.get_json()

        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id),None)

        if recipe is None:
            return {'message': self.sarasa}, HTTPStatus.NOT_FOUND
        
        recipe.name = data['name']
        recipe.description = data['description']
        recipe.num_of_servings = data['num_of_servings']
        recipe.cook_time = data['cook_time']
        recipe.directions = data['directions']

        return recipe.data, HTTPStatus.OK

