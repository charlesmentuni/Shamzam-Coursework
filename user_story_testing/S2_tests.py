import requests
import base64
import json
import sqlite3

ADD_URL = "http://localhost:3003/admin/add"

# Unhappy paths: adding a file that already exists, Having no content in the file.
# Happy paths: adding a file that doesn't exist

def setup():

    con = sqlite3.connect("../songs.db")
    cur = con.cursor()
    con.execute("DROP TABLE IF EXISTS songs")
    con.commit()
    cur.execute("CREATE TABLE songs (name TEXT, artist TEXT, file TEXT, PRIMARY KEY (name, artist))")
    con.commit()
    con.close()


def test2():
    
    full_file = base64.b64encode(open("../full_songs/Blinding Lights.wav", 'rb').read()).decode('utf-8')
    hdrs = {"Content-Type" : "application/json"}
    js   =  {"name" : "Blinding Lights", "artist": "The Weeknd", "audio" : full_file}
    rsp = requests.post(ADD_URL, headers=hdrs, json=js)

    file = open("answer.wav", 'wb')
    file.write(base64.b64decode(rsp.json()["file"]))
    file.close()



if __name__ == "__main__":
    setup()
    test2()