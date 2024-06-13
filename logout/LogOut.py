from flask import request,make_response
from ResponceHandler import Responce
def process():
    try:
        res = make_response()
        res.set_cookie("session","",expires=0)
        return Responce.send(200,{},"logout")
    except:
        return Responce.send(500,{},"server in truble")