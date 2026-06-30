from flask import Flask, render_template, request, redirect, session
from database.db import users, posts, comments
from bson.objectid import ObjectId
from datetime import datetime

import cloudinary
import cloudinary.uploader
import bcrypt  

import os
from dotenv import load_dotenv

load_dotenv()


cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = users.find_one({"email": email})

        if user:
          stored_password = bytes(user["password"])

          if bcrypt.checkpw(password.encode("utf-8"), stored_password):
            session["user"] = user["name"]
            session["email"] = user["email"]
            return redirect("/dashboard")

        return "Invalid Email or Password!"

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = users.find_one({"email": email})

        if existing_user:
            return "Email already registered!"

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        users.insert_one({
            "name": name,
            "email": email,
            "password": hashed_password
        })

        session["user"] = name
        session["email"] = email

        return redirect("/dashboard")

    return render_template("register.html")

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    search = request.args.get("search")

    if search:
        all_posts = list(posts.find({
            "title": {"$regex": search, "$options": "i"}
        }))
    else:
        page = int(request.args.get("page", 1))
        limit = 6
        skip = (page - 1) * limit
    if search:

      all_posts = list(posts.find({
        "title": {"$regex": search, "$options": "i"}
      }))
    else:
      all_posts = list(posts.find().skip(skip).limit(limit))
      
    return render_template(
        "dashboard.html",
        posts=all_posts,
        username=session["user"],
        page=page
    )

@app.route("/create", methods=["GET", "POST"])
def create_blog():

    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]

        image_file = request.files["image"]

        upload_result = cloudinary.uploader.upload(image_file)
        image_url = upload_result["secure_url"]

        posts.insert_one({
            "title": title,
            "image": image_url,
            "description": description,
            "author": session["user"],
            "created_at": datetime.now().strftime("%d %B %Y"),
            "likes": 0,
            "liked_by": []   
        })

        return redirect("/dashboard")

    return render_template("create_post.html")

@app.route("/delete/<id>")
def delete_blog(id):

    posts.delete_one({"_id": ObjectId(id)})
    return redirect("/dashboard")

@app.route("/edit/<id>", methods=["GET", "POST"])
def edit_blog(id):

    post = posts.find_one({"_id": ObjectId(id)})

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]

        if request.files["image"] and request.files["image"].filename != "":
            image_file = request.files["image"]
            upload_result = cloudinary.uploader.upload(image_file)
            image_url = upload_result["secure_url"]
        else:
            image_url = post["image"]

        posts.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "title": title,
                "image": image_url,
                "description": description
            }}
        )

        return redirect("/dashboard")

    return render_template("edit_post.html", post=post)

@app.route("/post/<id>", methods=["GET", "POST"])
def post(id):

    blog = posts.find_one({"_id": ObjectId(id)})

    if request.method == "POST":

        username = request.form["username"]
        message = request.form["message"]

        comments.insert_one({
            "post_id": id,
            "username": username,
            "message": message
        })

        return redirect(f"/post/{id}")

    all_comments = list(comments.find({"post_id": id}))

    return render_template("post.html", post=blog, comments=all_comments)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/like/<id>")
def like_post(id):

    if "user" not in session:
       return redirect("/login")

    post = posts.find_one({"_id": ObjectId(id)})
    user = session["email"]   # unique user

    liked_by = post.get("liked_by", [])

    if user in liked_by:

        posts.update_one(
            {"_id": ObjectId(id)},
            {
                "$pull": {"liked_by": user},
                "$inc": {"likes": -1}
            }
        )
    else:
        posts.update_one(
            {"_id": ObjectId(id)},
            {
                "$push": {"liked_by": user},
                "$inc": {"likes": 1}
            }
        )
   
    return redirect("/dashboard")

@app.route("/save/<id>")
def save_post(id):

    if "saved" not in session:
        session["saved"] = []

    if str(id) in session["saved"]:
        session["saved"].remove(str(id))
    else:
        session["saved"].append(str(id))

    session.modified = True
    return redirect("/dashboard")

@app.route("/saved")
def saved():

    if "saved" not in session:
        session["saved"] = []

    saved_posts = list(posts.find({
        "_id": {"$in": [ObjectId(i) for i in session["saved"]]}
    }))

    return render_template("saved.html", posts=saved_posts)

@app.route("/profile")
def profile():

    if "user" not in session:
        return redirect("/login")

    total_posts = posts.count_documents({
        "author": session["user"]
    })

    user_posts = list(posts.find({
        "author": session["user"]
    }))

    return render_template(
        "profile.html",
        username=session["user"],
        email=session["email"],
        total_posts=total_posts,
        posts=user_posts
    )

if __name__ == "__main__":
    app.run(debug=True)