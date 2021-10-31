from flask import Flask
from flask_restful import Api
from resources.Course import CourseGetter, CourseController
from models.Course import Course

# from resources.recipe import RecipeListResource
# from resources.recipeResource import RecipeResource
# from resources.recipePublic import RecipePublishResource

app = Flask(__name__)
api = Api(app)

courseService = Course({})
api.add_url_rule(CourseController, '/courses/create', resource_class_kwargs={'course': courseService})
api.add_url(CourseGetter, '/courses/view/<int:course_id>', resource_class_kwargs={'course': courseService})

# Sacar view
# Aca ponemos los endpoints
# api.add_resource(RecipeListResource, '/recipes')
# api.add_resource(RecipeResource, '/recipes/<int:recipe_id>', resource_class_kwargs={'sarasa': 'recipe not encontrada'})
# api.add_resource(RecipePublishResource, '/recipes/<int:recipe_id>/publish')



if __name__ == '__main__':
    app.run(port=5000, debug=True)

# curl -i -X POST localhost:5000/courses/create -H "Content-Type: application/json" -d '{"course_name":"Cheese Pizza"}'
