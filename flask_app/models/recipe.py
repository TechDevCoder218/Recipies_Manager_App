# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import registeruser
import re

# model the class after the friend table from our database
class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.recipe_name = data['recipe_name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.under_max_time = data['under_max_time']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.users = []

    # Now we use class methods to query our database
    @classmethod
    def get_all_recipes(cls):
        # creating a variable that represents the actual SQL query
        query = "SELECT * FROM recipes;"

        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('recipe_schema').query_db(query)

        # Create an empty list to append our instances of recipes. List to receive the results of the SELECT
        recipes = []

        # Iterate over the db results and create instances of recipes with cls, add them to the empty list
        for row in results:
            recipes.append( cls(row) )

        # return our new list that we created from our results
        return recipes


    # Method to create a recipe
    @classmethod
    def create_recipe(cls, data):
        # make our query
        query = "INSERT INTO recipes (recipe_name, description, instruction, under_max_time, user_id, created_at, updated_at) VALUES (%(recipe_name)s, %(description)s, %(instruction)s, %(max_time)s, %(user_id)s, %(created_date)s, NOW());"
        result = connectToMySQL('recipe_schema').query_db(query, data)
        return result

    # Method to update a recipe
    @classmethod
    def update_recipe(cls, data):
        # make our query
        query = "UPDATE recipes SET recipe_name = %(recipe_name)s, description = %(description)s, instruction = %(instruction)s, under_max_time = %(max_time)s, user_id = %(user_id)s, created_at = %(created_date)s  WHERE id = %(recipe_id)s;"
        connectToMySQL('recipe_schema').query_db(query, data)

    @classmethod
    def get_one_recipe_with_user( cls, data ):
        query = "SELECT * FROM  recipes LEFT JOIN users ON users.id = recipes.user_id WHERE recipes.user_id = %(id)s AND recipes.id = %(recipe_id)s;"
        results = connectToMySQL('recipe_schema').query_db( query , data )
        
        this_recipe = cls( results[0] )
        
        for row_from_db in results:
            user_data = {
                "id" : row_from_db["id"],
                "first_name" : row_from_db['first_name'],
                "last_name" : row_from_db['last_name'],
                "email" : row_from_db['email'],
                "pwd" : row_from_db['pwd'],
                "created_at" : row_from_db['created_at'],
                "updated_at" : row_from_db['updated_at'],
            }

            this_recipe.users.append( registeruser.Registeruser( user_data ))
        
        return this_recipe

    # Method to delete a recipe
    @classmethod
    def destroy_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(recipe_id)s"
        connectToMySQL("recipe_schema").query_db(query, data)

    @staticmethod
    def validate_recipe(data):
        is_valid = True

        if data['recipe_name'] == '' or len(data['recipe_name']) < 3:
            is_valid = False
            flash("Recipe name should be at least 3 characters long", "recipe")
        elif len(data['recipe_name']) > 50:
            is_valid = False
            flash("Recipe name should be 3 to 50 characters long", "recipe")

        if data['description'] == '' or len(data['description']) < 3:
            is_valid = False
            flash("Description should be at least 3 characters long", "recipe")
        elif len(data['description']) > 1000:
            is_valid = False
            flash("Description should be 3 to 1000 characters long", "recipe")

        if data['instruction'] == '' or len(data['instruction']) < 3:
            is_valid = False
            flash("Instructions should be at least 3 characters long", "recipe")
        elif len(data['instruction']) > 1000:
            is_valid = False
            flash("Instructions should be 3 to 1000 characters long", "recipe")

        return is_valid
