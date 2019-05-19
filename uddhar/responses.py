

def createResponse(status,message):
    json_response = {
        "status":status,
        "message":message
    }

    return json_response