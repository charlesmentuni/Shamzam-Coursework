import requests
import base64
import json
import sqlite3

CONVERT_URL = "http://localhost:3002/user/convert"
ADD_URL = "http://localhost:3002/admin/add"
REMOVE_URL = "http://localhost:3002/admin/remove"
LISTALL_URL = "http://localhost:3002/admin/get"

def setup():

    con = sqlite3.connect("songs.db")
    cur = con.cursor()
    con.execute("DROP TABLE IF EXISTS songs")
    con.commit()
    cur.execute("CREATE TABLE songs (name TEXT, artist TEXT, file TEXT, PRIMARY KEY (name, artist))")
    con.commit()
    con.close()

def test1():

    # json input? ask about this
    cropped_file = base64.b64encode(open("fragments/_Blinding Lights.wav", 'rb').read()).toString#decode('utf-8')
    # cropped_file = open("fragments/_Blinding Lights.wav", 'r').read()

    hdrs = {"Content-Type" : "application/json"}#, "audio" : cropped_file}
    js   =  {"audio" : cropped_file }

    rsp  = requests.post(CONVERT_URL, headers=hdrs, json=js)

    rsp_file = open("answer.wav", 'wb')
    rsp_file.write(base64.b64decode(rsp.text))
    rsp_file.close()

def test2():
    
    full_file = base64.b64encode(open("full_songs/Blinding Lights.wav", 'rb').read()).decode('utf-8')
    hdrs = {"Content-Type" : "application/json"}
    js   =  {"name" : "Blinding Lights", "artist": "The Weeknd", "audio" : full_file}
    rsp = requests.post(ADD_URL, headers=hdrs, json=js)

    file = open("answer.wav", 'wb')
    file.write(base64.b64decode(rsp.json()["file"]))
    file.close()

def test3():
    remove_song_name = "Blinding Lights"
    remove_artist = "The Weeknd"
    hdrs = {"Content-Type" : "application/json"}
    js = {"name" : remove_song_name, "artist" : remove_artist}
    rsp = requests.post(REMOVE_URL, headers=hdrs, json=js)
    print(rsp.json())

def test4():
    rsp = requests.get(LISTALL_URL)
    print(rsp.json())


if __name__ == "__main__":
    setup()