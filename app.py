from flask import Flask, render_template, request
app = Flask(__name__)

import requests


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_age = request.form.get("age")
    input_year = request.form.get("year")
    years_since_graduation = 2024 - int(input_year)
    return render_template("hello.html", name=input_name, age=input_age,
                           years=years_since_graduation)


def make_request(username):
    response = requests.get(f"https://api.github.com/users/{username}/repos")
    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            print(repo["full_name"])

@app.route("/githubapi", methods=["GET", "POST"])
def githubapi():
    if request.method == "POST":
        username = request.form.get("ghubusername")
        make_request(username)
        return render_template("githubapi.html", username=username)
    return render_template("githubapi.html")