import base64
import os 
import requests
from flask import Flask, request
import sqlite3

AUDD_KEY = ''
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

    
    audio = request.get_json()["audio"]
   
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

@app.route("/admin/add",methods=["POST"])
def admin_add():
    name = request.get_json()["name"]
    file = request.get_json()["audio"]
    artist = request.get_json()["artist"]

    con = sqlite3.connect("songs.db")
    cur = con.cursor()
    # Potentially could do an SQL injection
    query = "INSERT INTO songs VALUES (?, ?, ?)"
    cur.execute(query, (name, artist, file))
    cur.close()
    con.commit()
    return {"name": name, "file": file, "artist":artist}, 201

@app.route("/admin/remove",methods=["POST"])
def admin_remove():
    # Potentially add an id rather than a name so that it can be unique or something idk like in the case where two songs have the same name
    # Perhaps a composite key of the name and artist as it is exceedingly unlikely that an artist created the same song with the exact same title
    name = request.get_json()["name"]
    con = sqlite3.connect("songs.db")
    cur = con.cursor()
    query = "DELETE FROM songs WHERE name = '"+name+"'"
    #query = "SELECT * FROM songs WHERE name ='"+name+"'"
    cur.execute(query)
    cur.close()
    con.commit()
    return {"name": name}, 200

@app.route("/admin/get",methods=["GET"])
def admin_list_all():
    # Potentially also add artist names and such, so the admin can have a more full picture.
    con = sqlite3.connect("songs.db")
    cur = con.cursor()
    query = "SELECT name FROM songs"
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    return {"songs": result}, 200


if __name__ == "__main__":
    app.run(host="localhost",port=3002)
