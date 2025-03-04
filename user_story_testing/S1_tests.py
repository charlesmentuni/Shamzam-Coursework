import requests
import base64
import json
import sqlite3
import unittest


CONVERT_URL = "http://localhost:3002/user/convert"

# Unhappy paths: Invalid API key

class Testing(unittest.TestCase):
    def setup(self):

        con = sqlite3.connect("../songs.db")
        cur = con.cursor()
        con.execute("DROP TABLE IF EXISTS songs")
        con.commit()
        cur.execute("CREATE TABLE songs (name TEXT, artist TEXT, file TEXT, PRIMARY KEY (name, artist))")
        con.commit()
        con.close()

    #
    # HAPPY PATH 1: Recognise Blinding Lights from a fragment and return name, artist and full song
    #
    def test1(self):

        # json input? ask about this
        cropped_file = base64.b64encode(open("../fragments/_Blinding Lights.wav", 'rb').read()).decode('utf-8')
        # cropped_file = open("fragments/_Blinding Lights.wav", 'r').read()

        hdrs = {"Content-Type" : "application/json"}#, "audio" : cropped_file}
        js   =  {"audio" : cropped_file }

        rsp  = requests.post(CONVERT_URL, headers=hdrs, json=js)

        self.assertEqual(rsp.status_code, 200)


