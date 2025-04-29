from flask import Flask, redirect, render_template, request, flash, jsonify
from flask_cors import CORS

import docker_py

app = Flask(__name__)
app.config["SECRET_KEY"] = "TEMP"
CORS(app)

def login():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data received"}), 400
        
    username = data.get('username')
    password = data.get('password')

    if username == "admin" and password == "123456":
        return jsonify({"success": True, "message": "Login successful!", "token": "yourToken"})

    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401


@app.route("/", methods=["GET"])
def home():
    if request.method == "GET":
        docker_client = docker_py.docker_py()
        docker_ps = docker_client.docker_ps()
        docker_client.docker_stats()
        return render_template("index.html", container_list=docker_ps)


@app.route("/create_container", methods=["POST", "GET"])
def new_container():
    if request.method == "POST":
        img = request.form.get("image")
        name = request.form.get("name")
        docker_client = docker_py.docker_py()
        docker_create_msg = docker_client.docker_create(name, img)
        flash(docker_create_msg)
        return redirect("/")
    elif request.method == "GET":
        return render_template("create_container.html")

@app.route("/remove_container", methods=["POST"])
def remove_container():
    if request.method == "POST":
        docker_client = docker_py.docker_py()
        name = request.form.get("action")
        docker_remove_msg = docker_client.docker_remove(name)
        flash(docker_remove_msg)
        return redirect("/")
    elif request.method == "GET":
        return redirect("/")


@app.route("/start_container", methods=["POST"])
def start_container():
    if request.method == "POST":
        docker_client = docker_py.docker_py()
        name = request.form.get("action")
        docker_start_msg = docker_client.docker_start(name)
        flash(docker_start_msg)
        return redirect("/")
    elif request.method == "GET":
        return redirect("/")


@app.route("/stop_container", methods=["POST"])
def stop_container():
    if request.method == "POST":
        docker_client = docker_py.docker_py()
        name = request.form.get("action")
        docker_stop_msg = docker_client.docker_stop(name)
        flash(docker_stop_msg)
        return redirect("/")
    elif request.method == "GET":
        return redirect("/")


if __name__ in "__main__":
    app.run(port=5000, debug=True)
