from flask import Flask,g, render_template
import sqlite3
DATABASE = 'database.db'
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

############################# Routes ###################################################################

@app.route("/")
def home():
    planets = query_db("""
        SELECT ID, Name, Diameter_km, ImageURL FROM Planets;""")
    return render_template("home.html", planets=planets)

@app.route("/planet/<int:id>")
def planet(id):
    sql = """
        SELECT * FROM Planets
        WHERE ID = ?;"""
    planet = query_db(sql,(id,),True)
    sql = """
        SELECT MoonID, Name, `Diameter-km`, ImageURL FROM Moons 
        WHERE PlanetID = ?;"""
    moons = query_db(sql,(id,),False)
    return render_template("planet.html", planet=planet, moons=moons)

############################# Runner ###################################################################
if __name__ == "__main__":
    app.run(debug=True)