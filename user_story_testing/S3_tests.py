import requests
import base64
import json
import sqlite3
import unittest

# Unhappy paths: removing a file when it doesn't exist, 
# Happy paths: removing a file when it does exist

REMOVE_URL = "http://localhost:3003/admin/remove"

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
    # HAPPY PATH 1: Removing a song that exists on the songs table
    #
    def test1(self):
        remove_song_name = "Blinding Lights"
        remove_artist = "The Weeknd"
        hdrs = {"Content-Type" : "application/json"}
        js = {"name" : remove_song_name, "artist" : remove_artist}
        rsp = requests.post(REMOVE_URL, headers=hdrs, json=js)

        self.assertEquals(rsp.status_code, 204)

    #
    # UNHAPPY PATH 1: Removing a song that doesn't exist on the songs table
    #
    def test2(self):
        remove_song_name = "good 4 u"
        remove_artist = "Olivia Rodrigo"
        hdrs = {"Content-Type" : "application/json"}
        js = {"name" : remove_song_name, "artist" : remove_artist}

        rsp = requests.post(REMOVE_URL, headers=hdrs, json=js)
        self.assertEquals(rsp.status_code, 404)
        self.assertEquals(rsp.json(), {"error": "Song not found in table"})


