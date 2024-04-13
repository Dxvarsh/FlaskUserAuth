from flask  import Flask
app = Flask(__name__)

@app.route("/api/v1/login",methods=["GET"])
def login():
    return "logged in"

app.run(host="127.0.0.1",port=5000,debug=True)