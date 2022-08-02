# registerusers.py
from flask import render_template,redirect,request,session,flash,url_for
from flask_app import app
from flask_bcrypt import Bcrypt
from flask import flash
from flask_app.models import recipe

bcrypt = Bcrypt(app)

from flask_app.models.registeruser import Registeruser

@app.route("/")
def index():

    return render_template("index.html")

# route to create a user
@app.route("/create", methods = ["POST"])
def create_user():
    hashedpw = bcrypt.generate_password_hash(request.form['pwd'])

    data = {
        'first_name' : request.form['fname'],
        'last_name' : request.form['lname'],
        'email' : request.form['email'],
        'pwd' : request.form['pwd'],
        'pwdconfirm' : request.form['pwdconfirm']
    }

    if not Registeruser.get_one_user_by_email(data):
        if Registeruser.validate_user_registration(data):
            data['pwd'] = hashedpw
            data['pwdconfirm'] = hashedpw
            user_id = Registeruser.create_user(data)
            session['id'] = user_id
            session['first_name'] = data['first_name']
            session['login'] = True
        else: 
            return redirect("/")
    else:
        flash("Invalid email", "register")
        return redirect("/")

    return redirect(url_for('dashboard'))


@app.route("/login", methods = ["POST"])
def login_user():

    data = {
        'email' : request.form['email'],
        'pwd' : request.form['pwd']
    }

    theuser = Registeruser.get_one_user_by_email(data)
    print(theuser)
    if not theuser:
        flash("Invalid email", "login")
        return redirect("/")
    else:
        if bcrypt.check_password_hash(theuser[0]['pwd'], data['pwd']):
            if Registeruser.validate_user_login(data):
                session['id'] = theuser[0]['id']
                session['first_name'] = theuser[0]['first_name']
                session['login'] = True
            else: 
                return redirect("/")
        else:
            flash("Invalid password", "login")
            return redirect("/")
    
    return redirect(url_for('dashboard'))

@app.route("/dashboard")
def dashboard():
    if not session:

        return redirect("/")

    if session['id'] and session['login'] == True:

        data = {
            'id' : session['id']
        }
    
    userinfo = Registeruser.get_user_with_recipes(data)
    
    
    return render_template("dashboard.html", user_fname = session['first_name'], userinfo = userinfo)

@app.route("/show_recipe/<int:id>/<int:recipe_id>")
def show_user(id,recipe_id):

    data = {
        'id' : id,
        'recipe_id' : recipe_id
    }

    userinfo = Registeruser.get_user_with_one_recipe(data)
    
    return render_template("one_recipe.html", user_fname = session['first_name'], userinfo = userinfo)

# route to send back to homepage
@app.route("/logout", methods = ["POST"])
def logout():
    session.clear()

    return redirect("/")

