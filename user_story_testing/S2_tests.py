import requests
import base64
import json
import sqlite3
import unittest


ADD_URL = "http://localhost:3003/admin/add"

# Unhappy paths: adding a file that already exists, Having no content in the file.
# Happy paths: adding a file that doesn't exist

class Testing(unittest.TestCase):
    def setUp(self):
        
        con = sqlite3.connect("../songs.db")
        cur = con.cursor()

        # Empties the database
        con.execute("DROP TABLE IF EXISTS songs")
        con.commit()

        # Creates new table and fills with Don't look back in anger by Oasis
        cur.execute("CREATE TABLE songs (name TEXT, artist TEXT, file TEXT, PRIMARY KEY (name, artist))")

        query = "INSERT INTO songs VALUES (?, ?, ?)"
        
        with open("../full_songs/Dont Look Back In Anger.wav", 'rb') as f:
            file = base64.b64encode(f.read()).decode('utf-8')
        
        cur.execute(query, ("Dont Look Back In Anger", "Oasis", file))
        con.commit()

        con.close()


    ###########################################################
    ## HAPPY PATH 1: Adding a song that doesn't exist        ##
    ###########################################################

    def test1(self):
        
        # Base64 encodes full song file and converts to string, so that it can be sent through a json file
        blinding_lights = open("../full_songs/Blinding Lights.wav", 'rb')
        full_file = base64.b64encode(blinding_lights.read()).decode('utf-8')
        blinding_lights.close()
        hdrs = {"Content-Type" : "application/json"}
        js   =  {"name" : "Blinding Lights", "artist": "The Weeknd", "audio" : full_file}
        rsp = requests.put(ADD_URL, headers=hdrs, json=js)
        self.assertEqual(rsp.status_code, 201)


    ###########################################################
    ## HAPPY PATH 2: Adding a new song by the same artist    ##
    ###########################################################

    def test2(self):
        # Artist and song name are used as a composite key in the database
        # This is testing if the database can handle 2 or more songs by the same artist

        # The file is arbitrary, as it doesn't matter what the actual song is
        with open("../full_songs/Blinding Lights.wav", 'rb') as blinding_lights:
            full_file = base64.b64encode(blinding_lights.read()).decode('utf-8')

        hdrs = {"Content-Type" : "application/json"}
        js   =  {"name" : "Wonderwall", "artist": "Oasis", "audio" : full_file}
        rsp = requests.put(ADD_URL, headers=hdrs, json=js)
        
        self.assertEqual(rsp.status_code, 201)


    ###########################################################
    ## UNHAPPY PATH 1: Adding a song that already exists     ##
    ###########################################################
    def test3(self):
        # Don't look back in Anger was already added in the setup, so can't be added again
        with open("../full_songs/Dont Look Back In Anger.wav", 'rb') as f:
            full_file = base64.b64encode(f.read()).decode('utf-8')

        hdrs = {"Content-Type" : "application/json"}
        js   =  {"name" : "Dont Look Back In Anger", "artist": "Oasis", "audio" : full_file}

        rsp = requests.put(ADD_URL, headers=hdrs, json=js)

        self.assertEqual(rsp.status_code, 409)
        self.assertEqual(rsp.json(), {"error" : "Song already exists in table"})


    ###########################################################
    ## UNHAPPY PATH 2: Adding a song with no content         ##
    ###########################################################

    def test4(self):

        hdrs = {"Content-Type" : "application/json"}
        js   =  {}
        rsp = requests.put(ADD_URL, headers=hdrs, json=js)

        self.assertEqual(rsp.status_code, 400)
        self.assertEqual(rsp.json(), {"error": "One or more fields are empty"})

    def tearDown(self):
        con = sqlite3.connect("../songs.db")
        cur = con.cursor()
        con.execute("DROP TABLE IF EXISTS songs")
        con.commit()
        con.close()


