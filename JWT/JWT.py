import jwt
secret_key = "thisismysecretkeywhichissettojwt"
def encode(payload):
    try:
        jwt_cookie = jwt.encode(payload,secret_key)
        return {"status":0,"data":f"{jwt_cookie}"}
    except:
        print(f"Error in encoding cookie : {jwt_cookie}")
        return {"status":1,"data":""}

def decode(jwt_cookie):
    try:
        decoded_cookie = jwt.decode(jwt_cookie,secret_key,algorithms="HS256")
        return {"status":0,"data":f"{decoded_cookie["data"]}"}
    except:
        print(f"Error in decoding cookie : {jwt_cookie} : {decoded_cookie}")
        return {"status":1,"data":""}