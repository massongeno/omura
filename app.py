from flask import Flask, redirect, render_template, jsonify, request, flash
from dataclasses import asdict
import docker_py

app = Flask(__name__)
app.config["SECRET_KEY"] = "TEMP"


@app.route("/containers", methods=["GET"])
def containers():
    if request.method == "GET":
        docker_client = docker_py.docker_py()
        docker_ps_stats = docker_client.docker_ps_stats()
        containers = [asdict(container) for container in docker_ps_stats]
        return jsonify(containers)


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
