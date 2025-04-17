from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
import os
import uuid

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

file_save_location = "static/images"
#app.secret_key = "hello_class"
allowed_types = [".png", ".jpg"]
#videoGames = []

@app.route("/", methods=["GET"])
def index():
    if "videoGames" not in session:
        print("clearing games")
        session["videoGames"] = []

    print(session.get("videoGames"))
    return render_template("index.html",garage=session.get("videoGames"), file_location=file_save_location)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    elif request.method == "POST":
        if "videoGames" not in session:
            print("Clearing session data")
            session["videoGames"] = []
        make = request.form.get("make", "invalid")
        model = request.form.get("model", "invalid")
        car_year = request.form.get("car_year", "invalid")
        series = request.form.get("series", "invalid")
        uploaded_file = request.files['file']

        if uploaded_file.filename != '':
            extension = os.path.splitext(uploaded_file.filename)[1]
            if extension in allowed_types:
                unique_name = f"{uuid.uuid4().hex}{extension}"
                filename = os.path.join(file_save_location, unique_name)
                uploaded_file.save(filename)
                session["videoGames"].append({"make": make, "model": model, "series": series, "car_year": car_year, "image": unique_name})
            else:
                flash("The file is of the wrong type", "error")
                return redirect("./add")


        print(session.get("videoGames"))
        session.modified = True
        flash("Good job! You have added a new car to your collection", "message")
        return redirect("/")
    
@app.route("/remove", methods=["GET", "POST"])
def remove():
    if request.method == "GET":
        return render_template("remove.html", games=session.get("videoGames"), file_location=file_save_location)

    elif request.method == "POST":
        if "videoGames" not in session:
            session["videoGames"] = []

        remove_image = request.form.get("remove", None)
        if remove_image:
            session["videoGames"] = [game for game in session["videoGames"] if game["image"] != remove_image]
            session.modified = True
            flash("Hot Wheel removed successfully.", "message")

        return redirect("/")

if __name__ == "__main__":
   app.run(debug=True, host="0.0.0.0")


