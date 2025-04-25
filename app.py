from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST', 'OPTIONS'])
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
@app.route('/containers', methods=['POST', 'GET'])
def containers():
    test_data = [
        {
            "id": "1",
            "name": "nginx-web",
            "command": "/bin/bash",
            "image": "nginx:latest",
            "created": "DD-MM-YYYY",
            "status": "running",
            "cpu": "60%",
            "disk": "45%",
            "mem": "45%",
            "ports": "5000"
        },
        {
            "id": "2",
            "name": "redis-cache",
            "command": "/bin/bash",
            "created": "DD-MM-YYYY",
            "image": "redis:7.0",
            "status": "created",
            "cpu": "45%",
            "disk": "45%",
            "mem": "45%",
            "ports": "5000, 5000, 5000"
        },
        {
            "id": "3",
            "name": "db-service",
            "command": "/bin/bash",
            "image": "postgres:14",
            "created": "DD-MM-YYYY",
            "status": "exited",
            "cpu": "45%",
            "disk": "45%",
            "mem": "45%",
            "ports": "5000"
        }
    ]
    return jsonify(test_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)