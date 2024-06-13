from flask  import request,jsonify
import uuid
from datetime import date
import os
from JWT import JWT
from ResponceHandler import Responce
sem1=[""]
sem2=[""]
sem3=[""]
sem4=[""]
sem5=[""]
sem6=[""]
def UploadPdf(app,cur,con):
    try:
        cookie = request.cookies.get("session")
        if cookie:
            decoded_cookie = JWT.decode(cookie)
            if decoded_cookie["status"] != 1:
                pass
        else:
            print
            return Responce(401,{},"Not Authenticated")
    except:
        return Responce.send(401,{},"not authenticated")
    userObject={}
    if 'pdf' not in request.files:
        return jsonify({'message': 'Not selected pdf'}), 400

    file = request.files['pdf']
    if file.filename == '':
        return jsonify({'message': 'Not selected pdf'}), 400

    filename = f"{uuid.uuid1(5)}.pdf"
    try:
        userObject["title"] = request.form.get("title")
        userObject["sub"] = request.form.get("subject")
        userObject["sem"] = request.form.get("sem")
        userObject["userid"] = decoded_cookie["data"]

        if(userObject["title"] is not None 
           and userObject["sub"] is not None
           and userObject["sem"] is not None
           and userObject["userid"] is not None):
            try:
                if userObject["sem"]== 1:
                    if userObject["sub"] in sem1:
                        pass
                    else:
                        return Responce.send(402,{},"subject name is not valid")
                if userObject["sem"]== 2:
                    if userObject["sub"] in sem2:
                        pass
                    else:
                        return Responce.send(402,{},"subject name is not valid")
                if userObject["sem"]== 3:
                    if userObject["sub"] in sem3:
                        pass
                    else:
                        return Responce.send(402,{},"subject name is not valid")
                if userObject["sem"]== 4:
                    if userObject["sub"] in sem4:
                        pass
                    else:
                        return Responce.send(402,{},"subject name is not valid")
                if userObject["sem"]== 5:
                    if userObject["sub"] in sem5:
                        pass
                    else:
                        return Responce.send(402,{},"subject name is not valid")
                if userObject["sem"]== 6:
                    if userObject["sub"] in sem6:
                        pass
                    else:
                        return Responce.send(402,{},"subject name is not valid")
            except:
                pass
            file.save(os.path.join(app.config['pdf'], filename))
            try:
                cur.execute(f"insert into pdfs values('{uuid.uuid1(7)}','{userObject["title"]}','{userObject["sub"]}','{userObject["sem"]}','{userObject["userid"]}','{date.today()}','{filename}');")
                con.commit()
            except Exception as e:
                print(e)
                return Responce.send(500,{},"server Error")
            return Responce.send(200,{},"file uploaded")
        else:
            print(userObject)
            return Responce.send(401,{},"parameter missing")
    except:
        print(userObject)
        return Responce.send(401,{},"parameter missing")