import requests
import base64
import json
import sqlite3

CONVERT_URL = "http://localhost:3002/user/convert"

# Unhappy paths: Invalid API key

def setup():

    con = sqlite3.connect("../songs.db")
    cur = con.cursor()
    con.execute("DROP TABLE IF EXISTS songs")
    con.commit()
    cur.execute("CREATE TABLE songs (name TEXT, artist TEXT, file TEXT, PRIMARY KEY (name, artist))")
    con.commit()
    con.close()

def test1():

    # json input? ask about this
    cropped_file = base64.b64encode(open("../fragments/_Blinding Lights.wav", 'rb').read()).toString#decode('utf-8')
    # cropped_file = open("fragments/_Blinding Lights.wav", 'r').read()

    hdrs = {"Content-Type" : "application/json"}#, "audio" : cropped_file}
    js   =  {"audio" : cropped_file }

    rsp  = requests.post(CONVERT_URL, headers=hdrs, json=js)

    rsp_file = open("answer.wav", 'wb')
    rsp_file.write(base64.b64decode(rsp.text))
    rsp_file.close()


if __name__ == "__main__":
    test1()