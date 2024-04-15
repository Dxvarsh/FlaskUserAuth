from flask import make_response,jsonify
def send(code,data,message):
    res = {
        "status_code":code,
        "data":data,
        "message":message
        }
    res = make_response(jsonify(res),code)
    return res
    