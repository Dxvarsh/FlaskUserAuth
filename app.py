from flask  import Flask,request,make_response,jsonify,redirect
from JWT import JWT
from datetime import datetime
from logout import LogOut
from getuser import GetUser
from upload import uploadpdf
from  ResponceHandler import Responce
import mysql.connector
import json
import uuid

from flask_cors import CORS

app = Flask(__name__)
CORS(app,supports_credentials=True)
app.config["FRONT_END_URL"] = "http://localhost:5173"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "kirtan"
app.config["MYSQL_DB"] = "users_db"
app.config["MYSQL_PASSWORD"] ="kirtan123"
app.config["pdf"]="./uploadpdf/"
con = mysql.connector.Connect(
    host = app.config["MYSQL_HOST"],
    user = app.config["MYSQL_USER"],
    password = app.config["MYSQL_PASSWORD"],
    database = app.config["MYSQL_DB"]
)
cur = con.cursor()

@app.route("/api/v1/login",methods=["POST"])
def login():
    try :
        data={}
        try:
            cookie = request.cookies.get("session")
            if cookie:
                decoded_cookie = JWT.decode(cookie)
                if decoded_cookie["status"] != 1:
                    try :
                        cur.execute(f"SELECT * FROM users where userid='{decoded_cookie["data"]}'")
                        row = cur.fetchone()
                    except:
                        return Responce(401,{},"Error in Fetching cookie data from database")
                    if row:
                        try:
                            if row[0] == decoded_cookie["data"]:
                                return Responce.send(200,{},"Login successfull")
                            else:
                                return Responce.send(401,{},"Invalid Cookie")
                        except:
                            return Responce.send(500,{},"Error while checking cookie data is valid?")
                    else:
                        return Responce.send(401,{},"Invalid Cookie")
        except:
            pass
        try:
            data = json.loads(request.data.decode("utf-8"))
        except Exception as e:
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
                    if username == row[1] and password == row[2]:
                        jwt_cookie = JWT.encode({"data":f"{row[0]}"})
                        if jwt_cookie.get("status") == 0:
                             print("Sending cookie")
                             res = make_response("")
                             expiration_date = datetime.today() + datetime.timedelta(days=7)
                             res.set_cookie("session",jwt_cookie["data"],path='/',expires=expiration_date)
                             return res
                        else:
                            return Responce.send(500,{},"Error in setting Cookie")
                    else:
                        return Responce.send(401,{},"username and password is invalid")    
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
                        return Responce.send(409,{},"username or email already used")
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
@app.route("/api/v1/upload",methods=["POST"])
def upload():
    return uploadpdf.UploadPdf(app,cur,con)

@app.route("/api/v1/getuser",methods=["GET","OPTION"])
def getuser():
    return GetUser.process(cur)

@app.route("/api/v1/logout")
def logout():
    return LogOut.process()

app.run(host="127.0.0.1",port=5000,debug=True)