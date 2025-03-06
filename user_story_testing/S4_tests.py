import unittest.async_case
import requests
import base64
import json
import sqlite3
import unittest


LISTALL_URL = "http://localhost:3003/admin/get"

class Testing(unittest.TestCase):
    def setUp(self):
        con = sqlite3.connect("../songs.db")
        cur = con.cursor()

        con.execute("DROP TABLE IF EXISTS songs")
        con.commit()

        cur.execute("CREATE TABLE songs (name TEXT, artist TEXT, file TEXT, PRIMARY KEY (name, artist))")

        f1 = open("../full_songs/Blinding Lights.wav", 'rb')
        f2 = open("../full_songs/Everybody (Backstreets Back) (Radio Edit).wav", 'rb')
        f3 = open("../full_songs/good 4 u.wav", 'rb')

        query = "INSERT INTO songs VALUES (?, ?, ?)"
        file = base64.b64encode(f1.read()).decode('utf-8')
        cur.execute(query, ("Blinding Lights", "The Weeknd", file))

        file = base64.b64encode(f2.read()).decode('utf-8')
        cur.execute(query, ("Everybody (Backstreets Back) (Radio Edit)", "Backstreet Boys", file))

        file = base64.b64encode(f3.read()).decode('utf-8')
        cur.execute(query, ("good 4 u", "Olivia Rodrigo", file))

        f1.close()
        f2.close()
        f3.close()

        con.commit()
        con.close()

    #
    # HAPPY PATH 1: Listing all songs in the table
    #
    def test1(self):
        rsp = requests.get(LISTALL_URL)

        self.assertEqual(rsp.status_code, 200)


class Testing1(unittest.TestCase):
    def setUp(self):
        con = sqlite3.connect("../songs.db")
        cur = con.cursor()

        con.execute("DROP TABLE IF EXISTS songs")
        con.commit()

        cur.execute("CREATE TABLE songs (name TEXT, artist TEXT, file TEXT, PRIMARY KEY (name, artist))")

    #
    # HAPPY PATH 2: Listing songs when there are no songs in the table
    #
    def test1(self):
        rsp = requests.get(LISTALL_URL)
    
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.json(), {"songs":[]})