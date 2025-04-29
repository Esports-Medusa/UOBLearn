from flask import request, jsonify
from app import app, db
from models import User
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'msg': 'Email already registered'}), 400

    new_user = User(
        role=data['role'],
        username=data['username'],
        email=data['email'],
        is_first_login=True
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    # Automatic login
    token = create_access_token(identity=new_user.id)

    return jsonify({
        'msg': 'Registered successfully',
        'token': token,
        'username': new_user.username,
        'email': new_user.email,
        'is_first_login': True
    }), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()

    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.id)
        return jsonify({
            'msg': 'Login success',
            'token': token,
            'username': user.username,
            'email': user.email,
            'is_first_login': user.is_first_login
        }), 200

    return jsonify({'msg': 'Invalid credentials'}), 401

@app.route('/preferences', methods=['POST'])
@jwt_required()
def save_preferences():
    user = User.query.get(get_jwt_identity())
    data = request.json
    user.preferences = ",".join(data["preferences"])
    user.is_first_login = False
    db.session.commit()
    return jsonify({"msg": "Preferences saved."})

