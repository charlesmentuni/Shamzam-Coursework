import requests
import base64
import json
import sqlite3
import unittest


CONVERT_URL = "http://localhost:3002/user/convert"

# Unhappy paths: Invalid API key

class Testing(unittest.TestCase):
    def setUp(self):

        con = sqlite3.connect("../songs.db")
        cur = con.cursor()
        con.execute("DROP TABLE IF EXISTS songs")
        con.commit()
        cur.execute("CREATE TABLE songs (name TEXT, artist TEXT, file TEXT, PRIMARY KEY (name, artist))")
        query = "INSERT INTO songs VALUES (?, ?, ?)"
        file = base64.b64encode(open("../full_songs/Blinding Lights.wav", 'rb').read()).decode('utf-8')
        cur.execute(query, ("Blinding Lights", "The Weeknd", file))
        con.commit()
        con.close()

    #
    # HAPPY PATH 1: Recognise Blinding Lights from a fragment and return name, artist and full song
    #
    def test1(self):

        # json input? ask about this
        cropped_file = base64.b64encode(open("../fragments/_Blinding Lights.wav", 'rb').read()).decode('utf-8')

        hdrs = {"Content-Type" : "application/json"}#, "audio" : cropped_file}
        js   =  {"audio" : cropped_file }

        rsp  = requests.post(CONVERT_URL, headers=hdrs, json=js)

        self.assertEqual(rsp.status_code, 200)
    
    #
    # UNHAPPY PATH 1: Fragment not recognised by Audd API
    #
    def test2(self):
        davos_fragment = base64.b64encode(open("../fragments/_Davos.wav", 'rb').read()).decode('utf-8')
        hdrs = {"Content-Type" : "application/json"}
        js   =  {"audio" : davos_fragment }
        rsp  = requests.post(CONVERT_URL, headers=hdrs, json=js)

        self.assertEqual(rsp.status_code, 404)
    
    #
    # UNHAPPY PATH 2: Fragment recognised by Audd API but not in the songs table
    #
    def test3(self):
        cropped_file = base64.b64encode(open("../fragments/_good 4 u.wav", 'rb').read()).decode('utf-8')
        hdrs = {"Content-Type" : "application/json"}
        js   =  {"audio" : cropped_file }
        rsp  = requests.post(CONVERT_URL, headers=hdrs, json=js)
        self.assertEqual(rsp.status_code, 404)


    #
    # UNHAPPY PATH 3: File is not sent in the request
    #
    def test4(self):
        hdrs = {"Content-Type" : "application/json"}
        js   =  {}
        rsp  = requests.post(CONVERT_URL, headers=hdrs, json=js)
        self.assertEqual(rsp.status_code, 400)
        self.assertEqual(rsp.json(), {"error": "No audio file provided, or bad syntax"})



    def tearDown(self):
        con = sqlite3.connect("../songs.db")
        cur = con.cursor()
        con.execute("DROP TABLE IF EXISTS songs")
        con.commit()
        con.close()


