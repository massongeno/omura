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
            "image": "nginx:latest",
            "status": "running",
            "cpu": "45%",
            "disk": "45%",
            "mem": "45%"
        },
        {
            "id": "2",
            "name": "redis-cache",
            "image": "redis:7.0",
            "status": "stopped",
            "cpu": "45%",
            "disk": "45%",
            "mem": "45%"
        },
        {
            "id": "3",
            "name": "db-service",
            "image": "postgres:14",
            "status": "running",
            "cpu": "45%",
            "disk": "45%",
            "mem": "45%"
        }
    ]
    return jsonify(test_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)