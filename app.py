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
        print(repos[0].keys())
        return repos
    return []
    
def make_commit_request(commit_url):
    response = requests.get(commit_url)
    if response.status_code == 200:
        commit_data = response.json()[0]
    return commit_data
    
def format_result(data):
    result = []
    for row in data:
        repo_name = row["full_name"].split("/")[1]
        commit_data = make_commit_request(row["commits_url"].replace("{/sha}", ""))
        new_dict = {"repo_name": repo_name, "last_updated": row["updated_at"], "commits_url": row["git_commits_url"], "hash": commit_data["sha"], "author": commit_data["commit"]["author"]["name"], "date": commit_data["commit"]["author"]["date"], "commits_msg": commit_data["commit"]["message"]}
        result.append(new_dict)
    return result


@app.route("/githubapi", methods=["GET", "POST"])
def githubapi():
    if request.method == "POST":
        username = request.form.get("ghubusername")
        data = format_result(make_request(username))
        return render_template("githubapi.html", username=username, data=data)
    return render_template("githubapi.html")