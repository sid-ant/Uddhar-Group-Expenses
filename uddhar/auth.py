from flask import (
    Blueprint, Flask, g, redirect, request, jsonify, make_response,current_app,_request_ctx_stack
)
from werkzeug.security import check_password_hash, generate_password_hash

from uddhar.db import get_db

import jwt 
import datetime

import uddhar.responses as json_responses

from functools import wraps


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
    
    sub = user['user_id']
    token = create_token(sub)
    responseObject['status']="Success"
    responseObject['token']=token.decode()

    return make_response(jsonify(responseObject)),200

def create_token(sub):
    payload = {
        'sub':sub,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
        'iat': datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload,current_app.config['SECRET_KEY'],algorithm='HS256')
    return token
    

from werkzeug.local import LocalProxy
current_identity = LocalProxy(lambda: getattr(_request_ctx_stack.top, 'current_identity', None))

def login_required(func): 
    @wraps(func)
    def verify_token(*args, **kwargs):
        auth_token = request.headers.get('Authorization')
        if auth_token is None:
            errorResponse = json_responses.errorResponse
            errorResponse['status']='7001'
            errorResponse['message']='Authorization Header Required'
            return make_response(jsonify(errorResponse)),401
        try: 
            payload = jwt.decode(auth_token,current_app.config.get('SECRET_KEY'))
            current_app.logger.debug("INFO : %s",payload.get('sub'))
            _request_ctx_stack.top.current_identity = payload.get('sub')
            return func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            errorResponse = json_responses.errorMessage
            errorResponse['message']='Expired Token, Please Login Again'
            return make_response(jsonify(errorResponse)),401
        except jwt.InvalidSignatureError:
            errorResponse = json_responses.errorMessage
            errorResponse['message']='Invalid Token, Please Login Again'
            return make_response(jsonify(errorResponse)),401
    return verify_token

            