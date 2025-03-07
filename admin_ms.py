import sqlite3
from flask import Flask, request
import os

AUDD_KEY = os.environ["AUDD_KEY"]
URI = "https://api.audd.io/"

app = Flask(__name__)

# Endpoints
# /admin/add
# /admin/remove
# /admin/list


@app.route("/admin/add",methods=["POST"])
def admin_add():
    # This function adds a song the songs table in the database

    name = request.get_json().get("name")
    file = request.get_json().get("audio") 
    artist = request.get_json().get("artist") 

    con = sqlite3.connect("songs.db")
    cur = con.cursor()

    # Every song must have at least a name, artist and file otherwise it would be an invalid song.
    if not (file and name and artist):
        con.close()
        return {"error": "One or more fields are empty"}, 400

    query = "INSERT INTO songs VALUES (?, ?, ?)"
    try:
        cur.execute(query, (name, artist, file))
    except sqlite3.IntegrityError as e:
        # An integrity error will be raised if the song already exists in the songs table
        con.close()
        return {"error" : "Song already exists in table"}, 409
    
    con.commit()
    con.close()

    return "", 201

@app.route("/admin/remove",methods=["DELETE"])
def admin_remove():
    
    name = request.get_json().get("name")
    artist = request.get_json().get("artist")

    if not (name and artist):
        return {"error": "One or more fields are missing"}, 400

    con = sqlite3.connect("songs.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    

    # Check if the song exists in the database before deleting it
    query1 = "SELECT * FROM songs WHERE name = ? AND artist = ?"
    res = cur.execute(query1, (name, artist))

    # When there is no row to delete, then it will return a not found error
    row = res.fetchone()
    if not row:
        return {"error": "Song not found in table"}, 404
    
    fields = [col[0] for col in cur.description]

    # Delete the row containing the song from the table
    query = "DELETE FROM songs WHERE name = ? AND artist = ?"
    cur.execute(query, (name, artist))

    con.commit()
    con.close()

    # Sends back song that was just deleted in case the admin wants to access the file
    return {key: value for key, value in zip(fields, row)}, 204

@app.route("/admin/list",methods=["GET"])
def admin_list_songs():
    # Lists n number of songs from the songs table based on the num_of_songs parameter

    # Default limit is all the songs
    limit = ""
    try:
        if request.args.get("num_of_songs"):
            # Will raise an error if the limit is not an integer
            num_of_songs = int(request.args.get("num_of_songs"))

            # Limit has to be non-negative as you can't list a negative number of songs
            if num_of_songs < 0:
                raise ValueError
            
            limit = f"LIMIT {num_of_songs}"
    except:
        return {"error": "Invalid limit value"}, 400


    con = sqlite3.connect("songs.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    # Adds the limit to the sql query if it exists
    query = f"SELECT * FROM songs {limit}"
    cur.execute(query)

    result = cur.fetchall()
    fields = [col[0] for col in cur.description]

    con.close()
    # Will return all fields of the database, so if other fields are added, they will also be returned
    return {"songs": [{key: value for key, value in zip(fields, song)} for song in result]}, 200


if __name__ == "__main__":
    app.run(host="localhost",port=3003)
