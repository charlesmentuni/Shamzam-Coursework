import sqlite3
from flask import Flask, request


AUDD_KEY = ''
URI = "https://api.audd.io/"

app = Flask(__name__)

# Endpoints
# /admin/add
# /admin/remove
# /admin/get



@app.route("/admin/add",methods=["POST"])
def admin_add():

    if not request.get_json():
        return {"error": "One or more fields are empty"}, 400

    name = request.get_json()["name"]
    file = request.get_json()["audio"]
    artist = request.get_json()["artist"]

    con = sqlite3.connect("songs.db")
    cur = con.cursor()

    if not (file and name and artist):
        cur.close()
        return {"error": "One or more fields are empty"}, 400

    # Potentially could do an SQL injection
    query = "INSERT INTO songs VALUES (?, ?, ?)"
    try:
        cur.execute(query, (name, artist, file))
    except sqlite3.IntegrityError as e:
        con.close()
        return {"error" : "Song already exists in table"}, 409
    

    con.commit()
    con.close()

    # Returns the row that was just created in the database
    return "", 201

@app.route("/admin/remove",methods=["POST"])
def admin_remove():
    
    name = request.get_json()["name"]
    artist = request.get_json()["artist"]

    con = sqlite3.connect("songs.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    fields = [col[0] for col in cur.description]

    # Check if the song exists in the database before deleting it
    query1 = "SELECT * FROM songs WHERE name ='"+name+"' AND artist = '"+artist+"'"
    res = cur.execute(query1)

    # When there is no row to delete, then it will return a not found error
    row = res.fetchone()
    if not row:
        return {"error": "Song not found in table"}, 404
    
    # Delete the row containing the song from the table
    query = "DELETE FROM songs WHERE name = '"+name+"' AND artist = '"+artist+"'"
    cur.execute(query)
    
    cur.close()
    con.commit()

    # Sends back song that was just deleted in case the admin wants to access the file
    return {key: value for key, value in zip(fields, row)}, 204

@app.route("/admin/get",methods=["GET"])
def admin_list_all():

    con = sqlite3.connect("songs.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()

    query = "SELECT name, artist, file FROM songs"
    cur.execute(query)
    result = cur.fetchall()

    fields = [col[0] for col in cur.description]
    cur.close()
    
    return {"songs": [{key: value for key, value in zip(fields, song)} for song in result]}, 200


if __name__ == "__main__":
    app.run(host="localhost",port=3003)
