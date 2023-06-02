from flask import render_template, redirect, url_for, request
from flask_app import app
from flask_app.models.user import User

@app.route('/users')
def read_all():
    user_list = User.get_all()
    return render_template("read.html", users = user_list)

@app.route('/users/new')
def create():
    return render_template("create.html")

@app.route('/users/new/process', methods = ["POST"])
def process():
    if not User.validate_user(request.form):
        return redirect("/users/new")
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"]
    }
    User.create_user(data)
    return redirect(url_for("read_all"))

@app.route('/users/show/<int:user_id>')
def show(user_id):
    user=User.get_one(user_id)
    return render_template("show_user.html",user=user)

@app.route('/users/update/<int:user_id>')
def update(user_id):
    user=User.get_one(user_id)
    return render_template("update.html", user = user)

@app.route('/users/update_process',methods=['POST'])
def update_process():
    data = {
        "id": request.form["id"],
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"]
    }
    User.update(data)
    return redirect('/users')

@app.route("/users/delete/<int:id>")
def delete(id):
    User.delete_user({"id": id})
    return redirect('/users')

