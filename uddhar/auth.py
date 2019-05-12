from flask import (
    Blueprint, Flask, g, redirect, request, jsonify, make_response,current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

from uddhar.db import get_db

import jwt 
import datetime

bp = Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('/register',methods=['POST'])
def register():
    
    req =  request.get_json()
    password =  req.get("password")
    email = req.get("email")
    phone = req.get("phone")
    name =  req.get("name")

    responseObject = {
        'status':None, 
    }

    if name == None or password == None or email == None: 
        responseObject['status']="name, password & email requried"
        return make_response(jsonify(responseObject)),400
    
    db = get_db()

    if db.execute('SELECT user_id FROM user WHERE email = ?', (email,)).fetchone() is not None:
        responseObject['status']="user already exists"
        return make_response(jsonify(responseObject)),400

    db.execute(
                'INSERT INTO user (email, password, name,phone) VALUES (?, ?,?,?)',
                (email, generate_password_hash(password),name,phone)
            )
    db.commit()

    responseObject['status']="registered,successfully"
    return make_response(jsonify(responseObject)),201

@bp.route('/login',methods=['POST'])
def login():
    req =  request.get_json()
    password =  req.get("password")
    email = req.get("email")

    responseObject = {
        'status':None, 
        'token':None
    }

    if email==None or password==None:
        responseObject['status']="email and password required"
        return make_response(jsonify(responseObject)),400
    
    db = get_db()

    user =  db.execute('SELECT * FROM user WHERE email = ?', (email,)).fetchone()

    if user is None or check_password_hash(user['password'],password) is False:
        responseObject['status']="authentication failure"
        return make_response(jsonify(responseObject)),401
    
    payload = {
        'sub':user['user_id'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
        'iat': datetime.datetime.utcnow(),
    }
    current_app.logger.debug(current_app.config['SECRET_KEY'])
    token = jwt.encode(payload,current_app.config['SECRET_KEY'],algorithm='HS256')
    responseObject['status']="Success"
    responseObject['token']=token.decode()

    return make_response(jsonify(responseObject)),200

