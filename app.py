from flask  import Flask,request,make_response,jsonify,redirect
from  ResponceHandler import Responce
import mysql.connector
import json
import uuid
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.config["FRONT_END_URL"] = "http://evil.com"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "kirtan"
app.config["MYSQL_DB"] = "users_db"
app.config["MYSQL_PASSWORD"] ="kirtan123"
con = mysql.connector.Connect(
    host = app.config["MYSQL_HOST"],
    user = app.config["MYSQL_USER"],
    password = app.config["MYSQL_PASSWORD"],
    database = app.config["MYSQL_DB"]
)
cur = con.cursor()

@app.route("/api/v1/signin",methods=["POST"])
def login():
    try :
        data={}
        try:
            data = json.loads(request.data.decode("utf-8"))
        except:
            res = Responce.send(402,data,"Erorr While Proccessing Data Please Try again")
            return res
        if data:
            try :
                username = data["username"]
                password = data["password"]
            except:
                return Responce.send(401,{},"username or password is not in body")
            if username and password:
                cur.execute(f"SELECT * FROM users where username='{username}' and password='{password}'")
                row = cur.fetchone()
                try :
                    if username == row[0] and password == row[1]:
                        res = make_response("redirect")#redirect(f"{app.config["FRONT_END_URL"]}/")
                        res.set_cookie("session","testone",httponly=True)
                        return res
                except:
                    return Responce.send(401,{},"username and password is invalid")
            else :
                return "Username or Password should not be Empty"
        else :
            res = make_response("Error while processing data")
            res.status_code = "401"
            return res
    except:
        return Responce.send(500,{},'Ohh. Server in Truble')
    
@app.route("/api/v1/signup",methods=["POST"])
def signup():
    data = {}
    if request.data:
        data = json.loads(request.data.decode("utf-8"))
        if data.get("username") is not None and data.get("fullname") is not None and data.get("password") is not None and data.get("email") is not None:
            if(len(data["username"]) < 5):
                return Responce.send(401,{},"username is Too short")
            elif (len(data["password"])<8):
                return Responce.send(401,{},"password is Too short")
            elif(len(data["fullname"])<8):
                return Responce.send(401,{},"fullname is Too short")
            elif(len(data["email"])<8):
                return Responce.send(401,{},"email is Too short")
            else:
                try:
                    cur.execute(f"select * from users where username='{data["username"]}' or email='{data["email"]}'")
                    row = cur.fetchone()
                    if row :
                        return Responce.send(200,{},"User Already Exist...")
                    else:
                        cur.execute(f"insert into users values('{uuid.uuid4()}','{data["username"]}','{data["password"]}','{data["fullname"]}','{data["email"]}');")
                        con.commit()
                    return Responce.send(200,{},"Created successfully")
                except Exception as e:
                    return Responce.send(500,{},e)
        else :
            return Responce.send(405,{},"body should contain username,password,fullname,email")
    else:
        return Responce.send(401,{},"No data provided please provide nessery data")

app.run(host="127.0.0.1",port=5000,debug=True)