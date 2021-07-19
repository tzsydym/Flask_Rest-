from flask import Flask, jsonify, render_template, request,abort,make_response
from user_DAO import UserDAOMongo as UserDAO
from datetime import datetime
app = Flask(__name__)
dao = UserDAO()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/api/v0.0/users',methods=['GET'])
def get_users():
    users = dao.get_all()
    return jsonify(users), 200

@app.route('/api/v0.0/users/<string:user_name>',methods=['GET'])
def get_user(user_name):
    user = dao.get(user_name)
    if user is None:
        abort(404, message="User {} doesn't exist".format(user_name))
    return jsonify(user), 200

@app.route('/api/v0.0/users/<string:user_name>',methods=['DELETE'])
def delete_user(user_name):
    deleted_items = dao.delete(user_name)
    if deleted_items is None:
        abort(404, message="User {} doesn't exist".format(user_name))
    else:
        return '', 204

@app.route('/api/v0.0/users/<string:user_name>',methods=['PUT'])
def update_user(user_name):
    data = {
        'name': request.json['user']['name'],
        'dob': request.json['user']['dob'],
        'address': request.json['user']['address'],
        "description": request.json['user']['description']
    }
    matched_count = dao.update(user_name, data)
    return {'matched_count': matched_count}, 201

@app.route('/api/v0.0/users',methods=['POST'])
def add_user():
    if not request.json or not 'user' in request.json:
            abort(400)
    data = {
        'name': request.json['user']["name"],
        'dob': request.json['user']['dob'],
        'address': request.json['user']['address'],
        "description": request.json['user']['description'],
        "createdAt": ""
    }
    inserted_id = dao.create(data)
    return {'inserted_id': inserted_id}, 201

@app.route('/api/v0.0/nearby/<string:user_name>',methods=['GET'])
def get_nearby(user_name):
    if not request.json:
        abort(400)
    res = dao.get_nearby(user_name)
    return {'nearby': res}, 201

if __name__ == '__main__':
    app.run(debug=True)

