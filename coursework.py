import base64
import os 
import requests
from flask import Flask, request
import sqlite3

AUDD_KEY = os.environ["AUDD_KEY"]
URI = "https://api.audd.io/"

app = Flask(__name__)

# Endpoints
# /admin/add
# /admin/remove
# /admin/get
# /user/convert


def test_convert():
    f = open("_Blinding Lights.wav", 'rb')
    answer= user_convert(base64.b64encode(f.read()))
    f1 = open("answer.wav", 'wb')
    f1.write(base64.b64decode(answer))
    f1.close()

def test_admin_add():
    # Does the admin need add songs that the Audd.io can recognise
    f = open("Blinding Lights.wav", "rb")
    admin_add("Blinding Lights", base64.b64encode(f.read()))

def test_admin_remove():
    admin_remove("Well Done")

@app.route("/user/convert",methods=["POST"])
def user_convert():

    #parser.parse()
    #parser = request.make_form_data_parser()
    #audio = base64.b64encode(request.files["audio"].read())
    audio = bytes(request.get_json()["audio"], "utf-8")
    print(audio)

    #print(audio)
    audio = base64.b64encode(open("_Blinding Lights.wav", 'rb').read())
    data = {
        "Content-Type": "multipart/form-data",
        "api_token" : AUDD_KEY,
        "audio" : audio
    }
    
    response = requests.post(URI, data=data)
    print(response.json().keys())
    if "error" in response.json().keys():
        return response.json()["error"]
    name = response.json()["result"]["title"]

    con = sqlite3.connect("songs.db")
    cur = con.cursor()
    query = "SELECT * FROM songs WHERE name ='"+name+"'"
    res = cur.execute(query)



    return res.fetchone()[1]

def admin_add(name, file):
    con = sqlite3.connect("songs.db")
    cur = con.cursor()
    # Potentially could do an SQL injection
    query = "INSERT INTO songs VALUES (?, ?)"
    cur.execute(query, (name, file))
    cur.close()
    con.commit()

def admin_remove(name):
    # Potentially add an id rather than a name so that it can be unique or something idk like in the case where two songs have the same name
    # Perhaps a composite key of the name and artist as it is exceedingly unlikely that an artist created the same song with the exact same title
    con = sqlite3.connect("songs.db")
    cur = con.cursor()
    query = "DELETE FROM songs WHERE name = '"+name+"'"
    #query = "SELECT * FROM songs WHERE name ='"+name+"'"
    cur.execute(query)
    cur.close()
    con.commit()

def admin_list_all():
    # Potentially also add artist names and such, so the admin can have a more full picture.
    con = sqlite3.connect("songs.db")
    cur = con.cursor()
    query = "SELECT name FROM songs"
    cur.execute(query)
    result = cur.fetchall()
    cur.close()


if __name__ == "__main__":
    app.run(host="localhost",port=3002)
