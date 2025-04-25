from flask import Flask, redirect, render_template, request, flash

import docker_py

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    if request.method == "GET":
        docker_client = docker_py.docker_py()
        docker_ps = docker_client.docker_ps()
        return render_template("index.html", container_list=docker_ps)


@app.route("/create_container", methods=["POST", "GET"])
def new_container():
    if request.method == "POST":
        img = request.form.get("image")
        name = request.form.get("name")
        docker_client = docker_py.docker_py()
        docker_create_msg = docker_client.docker_create(name, img)
        flash(docker_create_msg)
        return render_template("index.html")
    elif request.method == "GET":
        return render_template("create_container.html")


if __name__ in "__main__":
    app.run(port=5000, debug=True)
