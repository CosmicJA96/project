from flask import Flask, g, render_template
import sqlite3
DATABASE = 'database.db'
app = Flask(__name__)

# Gets Database


def get_db():
    db = getattr(g, '_database', None)
    # If statement
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    # Database for Functions
    return db

# Query from Database


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# Page is Removed


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    # Closes Connection
    if db is not None:
        db.close()

# Error Handler


@app.errorhandler(404)
def not_found(error):
    # Shows Error Page
    return render_template("404.html"), 404


# Routes ##########################################

# Home Page Function


@app.route("/")
def home():
    # Gets Query from Database ###########################
    planets = query_db("""
        SELECT ID, Name, ImageURL FROM Planets;""")
    # Runs the template ###########################
    return render_template("home.html", planets=planets)

# Planet Page Function


@app.route("/planet/<int:id>")
def planet(id):
    # Query from Planets ###########################
    sql = """
        SELECT Name, Diameter_km, ImageURL, `Orbitalspeed-km/s`, Description,
        `Rotation-hrs`, `Age-BillionYrs` FROM Planets
        WHERE ID = ?;"""
    # Query ###########################
    planet = query_db(sql, (id,), True)
    # Query from Moons ###########################
    sql = """
        SELECT MoonID, Name, ImageURL FROM Moons
        WHERE PlanetID = ?;"""
    # Query ###########################
    moons = query_db(sql, (id,), False)
    # Runs the template ###########################
    return render_template("planet.html", planet=planet, moons=moons)

# Moon Page Function


@app.route("/moon/<int:id>")
def moon(id):
    # Query from Moons ###########################
    sql = """
        SELECT Name, `Diameter-km`, ImageURL, `Orbitalspeed-km/s`,
        Description FROM Moons
        WHERE MoonID = ?;"""
    # Query ###########################
    moon = query_db(sql, (id,), True)
    # Runs the template ###########################
    return render_template("moon.html", moon=moon)

# Runner ##########################################

# Runs the Website


if __name__ == "__main__":
    app.run(debug=True)
