# registerusers.py
from flask import render_template,redirect,request,session,flash,url_for
from flask_app import app
from flask import flash
from flask_app.models.recipe import Recipe


@app.route("/create_recipe")
def create_recipe():

    return render_template("create.html")

@app.route("/update_recipe/<int:id>/<int:recipe_id>")
def update_recipe(id,recipe_id):

    data = {
        'id' : id,
        'recipe_id' : recipe_id
    }

    recipeinfo = Recipe.get_one_recipe_with_user(data)

    return render_template("update.html", recipeinfo = recipeinfo)

@app.route("/create_new_recipe", methods = ["POST"])
def create_new_recipe():
    
    data = {
        'recipe_name' : request.form['rname'],
        'description' : request.form['description'],
        'instruction' : request.form['instruction'],
        'created_date' : request.form['created_date'],
        'max_time' : request.form['max_time'],
        'user_id' : session['id']
    }

    if not Recipe.validate_recipe(data):
            return redirect("/create_recipe")
    
    else:
        Recipe.create_recipe(data)
        return redirect(url_for('dashboard'))

@app.route("/update_existing_recipe", methods = ["POST"])
def update_existing_recipe():
    
    data = {
        'recipe_name' : request.form['rname'],
        'description' : request.form['description'],
        'instruction' : request.form['instruction'],
        'created_date' : request.form['created_date'],
        'max_time' : request.form['max_time'],
        'user_id' : session['id'],
        'recipe_id' : request.form['recipe_id']
    }

    if not Recipe.validate_recipe(data):
            return redirect(url_for('update_recipe', id = data['user_id'], recipe_id = data['recipe_id']))
    
    else:
        Recipe.update_recipe(data)
        return redirect(url_for('dashboard'))

@app.route("/delete_recipe/<int:recipe_id>")
def delete_recipe(recipe_id):

    data = {
        'recipe_id' : recipe_id
    }

    Recipe.destroy_recipe(data)
    return redirect(url_for('dashboard'))

    
