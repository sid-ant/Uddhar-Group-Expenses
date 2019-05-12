from flask import (
    Blueprint, Flask, g, redirect, request, jsonify, make_response,current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

from uddhar.db import get_db

bp = Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('/register',methods=['POST'])
def register():
    
    req =  request.get_json()
    current_app.logger.debug("Register user request : %s ",req)

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
