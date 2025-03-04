import requests
import base64
import json
import sqlite3


REMOVE_URL = "http://localhost:3003/admin/remove"


def setup():

    con = sqlite3.connect("songs.db")
    cur = con.cursor()
    con.execute("DROP TABLE IF EXISTS songs")
    con.commit()
    cur.execute("CREATE TABLE songs (name TEXT, artist TEXT, file TEXT, PRIMARY KEY (name, artist))")
    con.commit()
    con.close()




def test3():
    remove_song_name = "Blinding Lights"
    remove_artist = "The Weeknd"
    hdrs = {"Content-Type" : "application/json"}
    js = {"name" : remove_song_name, "artist" : remove_artist}
    rsp = requests.post(REMOVE_URL, headers=hdrs, json=js)
    print(rsp.json())



if __name__ == "__main__":
    test3()