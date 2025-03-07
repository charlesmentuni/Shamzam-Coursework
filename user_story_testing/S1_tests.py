import requests
import base64
import sqlite3
import unittest


CONVERT_URL = "http://localhost:3002/user/convert"


class Testing(unittest.TestCase):
    def setUp(self):

        con = sqlite3.connect("../songs.db")
        cur = con.cursor()

        con.execute("DROP TABLE IF EXISTS songs")
        con.commit()

        cur.execute("CREATE TABLE songs (name TEXT, artist TEXT, file TEXT, PRIMARY KEY (name, artist))")

        query = "INSERT INTO songs VALUES (?, ?, ?)"

        with open("../full_songs/Blinding Lights.wav", 'rb') as f:
            file = base64.b64encode(f.read()).decode('utf-8')

        cur.execute(query, ("Blinding Lights", "The Weeknd", file))

        with open("../full_songs/Everybody (Backstreets Back) (Radio Edit).wav", 'rb') as f:
            file = base64.b64encode(f.read()).decode('utf-8')
        
        cur.execute(query, ("Everybody (Backstreet's Back) (Radio Edit)", "Backstreet Boys", file))

        con.commit()
        con.close() 

    ###################################################################################################
    ## HAPPY PATH 1: Recognise Blinding Lights from a fragment and return name, artist and full song ##
    ###################################################################################################
    def test1(self):
        with open("../fragments/_Blinding Lights.wav", 'rb') as f:
            cropped_file = base64.b64encode(f.read()).decode('utf-8')

        hdrs = {"Content-Type" : "application/json"}
        js   =  {"audio" : cropped_file }

        rsp  = requests.post(CONVERT_URL, headers=hdrs, json=js)

        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.json().get("name"), "Blinding Lights")
        self.assertEqual(rsp.json().get("artist"), "The Weeknd")
        self.assertTrue("file" in rsp.json().keys())
    

    ############################################################################
    ## HAPPY PATH 2: Recognise Everybody (Backstreet's Back) from a fragment. ##
    ############################################################################
    def test2(self):
        # The name returned from AUDD API may not neccessarily be the name listed in the songs table
        # Also the song name has an apostrophe in it, which may cause issues when selecting

        with open("../fragments/_Everybody (Backstreets Back) (Radio Edit).wav", 'rb') as f:
            cropped_file = base64.b64encode(f.read()).decode('utf-8')
        
        hdrs = {"Content-Type" : "application/json"}
        js   =  {"audio" : cropped_file }

        rsp  = requests.post(CONVERT_URL, headers=hdrs, json=js)

        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.json().get("name"), "Everybody (Backstreet's Back) (Radio Edit)")
        self.assertEqual(rsp.json().get("artist"), "Backstreet Boys")
        self.assertTrue("file" in rsp.json().keys())


    ###########################################################
    ## UNHAPPY PATH 1: Fragment not recognised by Audd API   ##
    ###########################################################
    def test3(self):
        with open("../fragments/_Davos.wav", 'rb') as f:
            davos_fragment = base64.b64encode(f.read()).decode('utf-8')
        
        hdrs = {"Content-Type" : "application/json"}
        js   =  {"audio" : davos_fragment }
        rsp  = requests.post(CONVERT_URL, headers=hdrs, json=js)

        self.assertEqual(rsp.status_code, 404)
        self.assertEqual(rsp.json(), {"error": "Fragment not recognised"})
    
    #################################################################################
    ## UNHAPPY PATH 2: Fragment recognised by Audd API but not in the songs table. ##
    ################################################################################
    def test4(self):
        with open("../fragments/_good 4 u.wav", 'rb') as f:
            cropped_file = base64.b64encode(f.read()).decode('utf-8')

        hdrs = {"Content-Type" : "application/json"}
        js   =  {"audio" : cropped_file }
        rsp  = requests.post(CONVERT_URL, headers=hdrs, json=js)

        self.assertEqual(rsp.status_code, 404)
        self.assertEqual(rsp.json(), {"error": "Fragment recognised but not in the songs table"})


    ###########################################################
    ## UNHAPPY PATH 3: File is not sent in the request.       ##
    ###########################################################
    def test5(self):
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


