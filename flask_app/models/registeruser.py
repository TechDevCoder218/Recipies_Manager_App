# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import recipe
from flask import flash
import re

# model the class after the friend table from our database
class Registeruser:
    def __init__( self , db_data ):
        self.id = db_data['id']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.email = db_data['email']
        self.pwd = db_data['pwd']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

        self.recipes = []

    # Now we use class methods to query our database
    @classmethod
    def get_all_users(cls):
        # creating a variable that represents the actual SQL query
        query = "SELECT * FROM users;"

        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('recipe_schema').query_db(query)

        # Create an empty list to append our instances of users. List to receive the results of the SELECT
        users = []

        # Iterate over the db results and create instances of users with cls, add them to the empty list
        for row in results:
            users.append( cls(row) )

        # return our new list that we created from our results
        return users

    @classmethod
    def get_user_with_recipes( cls, data ):
        query = "SELECT * FROM users LEFT JOIN recipes ON users.id = recipes.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL('recipe_schema').query_db( query , data )
        
        this_user = cls( results[0] )
        
        for row_from_db in results:
            recipe_data = {
                "id" : row_from_db["recipes.id"],
                "recipe_name" : row_from_db['recipe_name'],
                "description" : row_from_db['description'],
                "instruction" : row_from_db['instruction'],
                "under_max_time" : row_from_db['under_max_time'],
                "user_id" : row_from_db['user_id'],
                "created_at" : row_from_db['created_at'],
                "updated_at" : row_from_db['updated_at'],
            }

            this_user.recipes.append( recipe.Recipe( recipe_data ))
        
        return this_user

    @classmethod
    def get_user_with_one_recipe( cls, data ):
        query = "SELECT * FROM users LEFT JOIN recipes ON users.id = recipes.user_id WHERE users.id = %(id)s AND recipes.id = %(recipe_id)s;"
        results = connectToMySQL('recipe_schema').query_db( query , data )
        
        this_user = cls( results[0] )
        
        for row_from_db in results:
            recipe_data = {
                "id" : row_from_db["id"],
                "recipe_name" : row_from_db['recipe_name'],
                "description" : row_from_db['description'],
                "instruction" : row_from_db['instruction'],
                "under_max_time" : row_from_db['under_max_time'],
                "user_id" : row_from_db['user_id'],
                "created_at" : row_from_db['created_at'],
                "updated_at" : row_from_db['updated_at'],
            }

            this_user.recipes.append( recipe.Recipe( recipe_data ))
        
        return this_user

    # Method to create a user
    @classmethod
    def create_user(cls, data):
        # make our query
        query = "INSERT INTO users (first_name, last_name, email, pwd, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(pwd)s, NOW(), NOW());"
        result = connectToMySQL('recipe_schema').query_db(query, data)
        return result

    # Method to update a user
    @classmethod
    def update_user(cls, data):
        # make our query
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, pwd = %(pwd)s, updated_at = NOW()  WHERE id = %(id)s;"
        connectToMySQL('recipe_schema').query_db(query, data)

    # Method to delete a user
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s"
        connectToMySQL("recipe_schema").query_db(query, data)

    # Method to get one user by id
    @classmethod
    def get_one_user_by_id(cls, data):
        # make our query
        query = "SELECT * FROM users WHERE id = %(id)s;"
        
        results = connectToMySQL('recipe_schema').query_db(query, data)

        user_info = results[0]

        # return our new list that we created from our results
        return user_info

    # Method to get one user by email
    @classmethod
    def get_one_user_by_email(cls, data):
        # make our query
        query = "SELECT * FROM users WHERE email = %(email)s;"
        
        results = connectToMySQL('recipe_schema').query_db(query, data)

        return results


    @staticmethod
    def validate_user_registration(data):
        is_valid = True

        first_name_regex = re.compile(r"^[A-Z]{1}[a-zA-Z. \-'!]{1,49}$")

        if not first_name_regex.match(data['first_name']):
            flash("First names should consist of spaces, dashes, apostophies, exclamation points, starting with a capital letter", "register")
            is_valid = False

        last_name_regex = re.compile(r"^[A-Z]{1}[a-zA-Z. \-'!]{1,49}$")

        if not last_name_regex.match(data['last_name']):
            flash("Last names should consist of spaces, dashes, apostophies, exclamation points, starting with a capital letter", "register")
            is_valid = False

        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not email_regex.match(data['email']):
            flash("Email is not valid!", "register")
            is_valid = False

        if data['pwd'] == '' or len(data['pwd']) < 8:
            is_valid = False
            flash("Password should not be empty; Password should not be less than 8 characters long", "register")
        elif len(data['pwd']) > 50:
            is_valid = False
            flash("First name should be 8 to 50 characters long", "register")

        if data['pwd'] != data['pwdconfirm']:
            is_valid = False
            flash("Confirm Password does not match Password", "register")
    
        return is_valid

    @staticmethod
    def validate_user_login(data):
        is_valid = True

        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not email_regex.match(data['email']):
            flash("Email is not valid!", "login")
            is_valid = False

        if data['pwd'] == '' or len(data['pwd']) < 8:
            is_valid = False
            flash("Password should not be empty; Password should not be less than 8 characters long", "login")
        elif len(data['pwd']) > 50:
            is_valid = False
            flash("First name should be 8 to 50 characters long", "login")

        return is_valid

