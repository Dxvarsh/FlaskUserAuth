from flask import request
from ResponceHandler import Responce

def process(cur):
    if request.args.get("subject"):
        if request.args.get("sem"):
            subject = request.args.get("subject")
            sem = request.args.get("sem")
            try:
                cur.execute(f'select username,title,sub,sem,pdf_path,upload_date from pdfs inner join users on pdfs.userid=users.userid where pdfs.sem="{sem}" and pdfs.sub="{subject}" ;')
                row = cur.fetchall()
                if not row:
                    return Responce.send(401,{},"pdf not found with this data")
                pdfs = []
                for i in row:
                    print(i[0])
                    pdf={
                        "username":i[0],
                        "title":i[1],
                        "subject":i[2],
                        "Sem":i[3],
                        "path":i[4],
                        "date":i[5].strftime("%A-%d-%m-%y")
                    }
                    pdfs.append(pdf)
                return Responce.send(200,pdfs,"success")
            except:
                return Responce.send(500,{},"sever in truble")
        else:
            return Responce.send(401,{},"perameter missing")
    else:
        return Responce.send(401,{},"peramter missing")