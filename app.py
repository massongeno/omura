from flask import Flask, redirect, render_template, request, flash, jsonify, send_from_directory, url_for
from flask_cors import CORS
from dataclasses import asdict
import docker_py
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from passlib.hash import bcrypt
from itsdangerous import URLSafeTimedSerializer

load_dotenv()

# configuration from environment
DB_USER        = os.getenv('DB_USER')
DB_PASS        = os.getenv('DB_PASS')
DB_HOST        = os.getenv('DB_HOST', 'localhost')
DB_PORT        = os.getenv('DB_PORT', '3306')
DB_NAME        = os.getenv('DB_NAME')
SECRET_KEY     = os.getenv('SECRET_KEY')

# initialize flask app
app = Flask(
    __name__,
    static_folder='dist',
    template_folder='templates'
)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+mysqldb://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config['SECRET_KEY']    = SECRET_KEY

# Enable cors for React dev server
CORS(app, 
     supports_credentials=True, 
     origins=["http://localhost:5173"],
     methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
     allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Origin", "Access-Control-Allow-Methods"]
)

# initialize extension
db            = SQLAlchemy(app)
migrate       = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
serializer    = URLSafeTimedSerializer(SECRET_KEY)

# user model
default_import_block = '''\n''' #placeholder
class User(db.Model, UserMixin):
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    @property
    def is_active(self):
        return True

    def set_password(self, password):
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password_hash)
    
# load user callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# registration endpoint
@app.route('/api/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    data = request.get_json() or {}
    if User.query.filter((User.username == data.get('username'))).first():
        return jsonify({'error': 'User with that username already exists'}), 400

    user = User(username=data.get('username'))
    user.set_password(data.get('password'))
    db.session.add(user)
    db.session.commit()
    return jsonify({'message':'User registered successfully', 'success': True}), 201

# login endpoint
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    user = User.query.filter_by(username=data.get('username')).first()
    if not user or not user.check_password(data.get('password')):
        return jsonify({"success": False, 'error': 'Invalid credentials'}), 401
    login_user(user)
    return jsonify({"success": True, 'id': user.id, 'username': user.username}), 200

# logout endpoint
@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'}), 200

# Serve React Build
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

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
        return jsonify({"message": "Container created successfully!"})
    
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
