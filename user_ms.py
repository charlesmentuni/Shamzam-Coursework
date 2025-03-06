import base64
import os 
import requests
from flask import Flask, request
import sqlite3

AUDD_KEY = ''
URI = "https://api.audd.io/"

app = Flask(__name__)

# Endpoints
# /user/convert


@app.route("/user/convert",methods=["POST"])
def user_convert():

    if not request.get_json() or not request.get_json()["audio"]:
        return {"error": "No audio file provided, or bad syntax"}, 400

    audio = request.get_json()["audio"]
    data = {
        "Content-Type": "multipart/form-data",
        "api_token" : AUDD_KEY,
        "audio" : audio
    }
    
    response = requests.post(URI, data=data)
    

    if "error" in response.json().keys():
        return response.json()["error"], response.status_code
    
    if not response.json()["result"]: 
        return {"error": "Fragment not recognised"}, 404
    
    name = response.json()["result"]["title"]

    con = sqlite3.connect("songs.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()

    query = "SELECT * FROM songs WHERE name ='"+name+"'"
    res = cur.execute(query)
    song = res.fetchone()
    fields = [col[0] for col in cur.description]

    if not song:
        return {"error":"Fragment recognised but not in the songs table"}, 404

    return {key: value for key, value in zip(fields, song)}, 200


if __name__ == "__main__":
    app.run(host="localhost",port=3002)
