import requests
import base64
import sqlite3
import unittest


REMOVE_URL = "http://localhost:3003/admin/remove"

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

        with open("../full_songs/Dont Look Back In Anger.wav", 'rb') as f:
            file = base64.b64encode(f.read()).decode('utf-8')

        cur.execute(query, ("Don't Look Back In Anger", "Oasis", file))

        con.commit()

        con.close()

    ###################################################################
    ## HAPPY PATH 1: Removing a song that exists on the songs table. ##
    ###################################################################
    def test1(self):
        remove_song_name = "Blinding Lights"
        remove_artist = "The Weeknd"
        hdrs = {"Content-Type" : "application/json"}
        js = {"name" : remove_song_name, "artist" : remove_artist}
        rsp = requests.delete(REMOVE_URL, headers=hdrs, json=js)

        self.assertEqual(rsp.status_code, 204)


    ###################################################################
    ## HAPPY PATH 2: Removing a song with an apostrophe in the name. ##
    ###################################################################
    def test2(self):
        remove_song_name = "Don't Look Back In Anger"
        remove_artist = "Oasis"
        hdrs = {"Content-Type" : "application/json"}
        js = {"name" : remove_song_name, "artist" : remove_artist}
        rsp = requests.delete(REMOVE_URL, headers=hdrs, json=js)

        self.assertEqual(rsp.status_code, 204)


    ############################################################################
    ## UNHAPPY PATH 1: Removing a song that doesn't exist on the songs table. ##
    ############################################################################
    def test3(self):
        remove_song_name = "good 4 u"
        remove_artist = "Olivia Rodrigo"
        hdrs = {"Content-Type" : "application/json"}
        js = {"name" : remove_song_name, "artist" : remove_artist}

        rsp = requests.delete(REMOVE_URL, headers=hdrs, json=js)

        self.assertEqual(rsp.status_code, 404)
        self.assertEqual(rsp.json(), {"error": "Song not found in table"})


    ###################################################################
    ## UNHAPPY PATH 2: Removing a song with no content in request.   ##
    ###################################################################
    def test4(self):
        hdrs = {"Content-Type" : "application/json"}
        js = {}
        rsp = requests.delete(REMOVE_URL, headers=hdrs, json=js)

        self.assertEqual(rsp.status_code, 400)
        self.assertEqual(rsp.json(), {"error": "One or more fields are missing"})

    def tearDown(self):
        con = sqlite3.connect("../songs.db")
        cur = con.cursor()
        con.execute("DROP TABLE IF EXISTS songs")
        con.commit()
        con.close()

