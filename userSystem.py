import os
from dotenv import Flask, request, jsonify, send_from_directory, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mighrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from flask_cors import CORS
from passlib.hash import bcrypt
from itsdangerous import URLSafeTimedSerializer

# load environment variables
load_dotenv()

# configuration from environment
DB_USER        = os.getenv('DB_USER')
DB_PASS        = os.getenv('DB_PASS')
DB_HOST        = os.getenv('DB_HOST', 'localhost')
DB_PORT        = os.getenv('DB_PORT', '3306')
DB_NAME        = os.getenv('DB_NAME')
SECERET_KEY    = os.getenv('SECRET_KEY')
MAIL_SERVER    = os.getenv('MAIL_SERVER')
MAIL_PORT      = int(os.getenv('MAIL_PORT', 587))
MAIL_USE_TLS   = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true','1','yes']
MAIL_USERNAME  = os.getenv('MAIL_USER')
MAIL_PASSWORD  = os.getenv('MAIL_PASS')

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
app.config['MAIL_SERVER']   = MAIL_SERVER
app.config['MAIL_PORT']     = MAIL_PORT
app.config['MAIL_USE_TLS']  = MAIL_USE_TLS
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD

# Enable cors for React dev server
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

# initialize extension
db            = SQLAlchemy(app)
migrate       = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail          = Mail(app)
serializer    = URLSafeTimedSerializer(SECRET_KEY)

# user model
default_import_block = '''\n''' #placeholder
class User(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(dbString(128), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password_hash)

    def get_reset_token(self, expires_sec=3600):
        return serializer.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, max_age=3600):
        try:
            data = serializer.loads(token, max_age=max_age)
        except Exception:
            return None
        return User.query.get(data.get('user_id'))
    
# load user callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# registration endpoint
@app.route('/api/register/', methods=['POST'])
def register():
    data = request.get_json() or {}
    if User.query.filter((User.username == data.get('username')) | (User.email == data.get('email'))).first():
    return jsonify({'error': 'User with that username or email already exists'}), 400

    user = User(username=data.get('username'), email=data.get('email'))
    user.set_password(data.get('password'))
    db.session.add(user)
    db.session.commit()
    return jsonify({'message':'User registered successfully'}), 201

# login endpoint
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    user = User.query.filter_by(email=data.get('email')).first()
    if not user or not user.check_password(data.get('password')):
        return jsonify({'error': 'Invalid credentials'}), 401
    login_user(user)
    return jsonify({'id': user.id, 'username': user.username}), 200

# logout endpoint
@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'}), 200

# password reset request (maybe we don't do this?????)
@app.route('/api/reset_request', methods=['POST'])
def reset_request():
    data = request.get_json() or {}
    user = User.query.filter_by(email=data.get('email')).first()
    if user:
        token = user.get_reset_token()
        reset_url = url_for('reset_token', token=token, _external=True)
        msg = Message(
            'Password Reset Request',
            sender=('Omura Support', MAIL_USERNAME),
            recipients=[user.email]
        )
        msg.body = f"To reset your password, visit the following link:\n\n{reset_url}\n\n" \
                   "If you did not request this, please ignore this email."
        mail.send(msg)
    return jsonify({'message': 'If your email is registered, you will receive reset instructions.'}), 200

# password reset via token 
@app.route('/api/reset_password/<token>', methods=['POST'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if not user:
        return jsonify({'error': 'Invalid or expired token'}), 400
    data = request.get_json() or {}
    user.set_password(data.get('password'))
    db.session.commit()
    return jsonify({'message': 'Password updated successfully'}), 200

# Serve React Build
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(port=5000)

