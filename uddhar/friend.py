from flask import (
    Flask, request, Blueprint, current_app, jsonify, make_response,_request_ctx_stack
)

from uddhar.db import get_db
from uddhar import responses
import sqlite3

from uddhar.auth import login_required,current_identity

bp = Blueprint('friend',__name__)

@bp.route('/add-friend',methods=['GET'])
@login_required
def addFriend():

    email = request.args.get('e')
    phone = request.args.get('p')

    db = get_db()

    if email is not None:
        query = "SELECT * FROM USER where EMAIL = ?"
        user = db.execute(query, (email,)).fetchone()
    elif phone is not None:
        query = "SELECT * FROM USER where PHONE = ?"
        user = db.execute(query, (phone,)).fetchone()
    else:
        errorResponse = responses.make_response('x4041','No Input')
        return make_response(jsonify(errorResponse)),400
    
    if user_id is None:
        return make_response(jsonify(responses.make_response('x3031','User not found'))),404
    
    user_id = user['user_id']

    query = 'INSERT into FRIEND (user_a, user_b) VALUES (?,?)'

    current_app.logger.debug("current user is %s",current_identity)
    current_app.logger.debug("request friend is %s",user_id)

    try:
        db.execute(query,(int(current_identity),user_id))
        db.commit()
    except sqlite3.Error as er:
        current_app.logger.debug("SQL Lite Error : ")
        current_app.logger.debug("%s",er)
        errorResponse = responses.createResponse('x9001','Contraint Failure')
        return make_response(jsonify(errorResponse)),400

    successResponse = responses.createResponse('2011','Friend Added')
    return make_response(jsonify(successResponse)),201


    
@bp.route('/friends',methods=['GET'])
@login_required
def list_friends():
    db = get_db()
    query = 'SELECT name,email FROM user INNER JOIN friend ON user.user_id = friend.user_b WHERE friend.user_a = ?'
    try:
        friends = db.execute(query,(int(current_identity),)).fetchall()
        friends = list(map(lambda x : dict(x),list(friends)))
        current_app.logger.debug(friends)
    except sqlite3.Error as er:
        current_app.logger.error("%s",er)
        return make_response(jsonify(responses.createResponse('x9001','Failure'))),400
    return make_response(jsonify(responses.createResponse('1001',friends))),200
        
