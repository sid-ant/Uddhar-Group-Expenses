from flask import (
    Flask, request, Blueprint, current_app, jsonify, make_response,_request_ctx_stack
)

from uddhar.db import get_db
from uddhar import responses

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
        errorResponse = responses.errorResponse
        errorResponse['status']="x4041"
        errorResponse['message']="User Not Found"
        return make_response(jsonify(errorResponse)),404
    
    user_id = user['user_id']
    current_user = current_identity # how do I get this 
    query = "INSERT into FRIEND (user_a,user_b) VALUES (?,?)"

    db.execute(query,(current_user,user_id))
    db.commit()
    response = response.successResponse
    response['status']="2011"
    response['message']="Successfully, Added Friend"
    return make_response(jsonify(response)),201


    
@bp.route('/yahoo',methods=['GET'])
@login_required
def helloworld():
    current_app.logger.info('Current User Is: %s',current_identity)