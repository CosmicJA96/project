from flask import Flask, g, render_template
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


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


# Routes ##########################################

# Home


@app.route("/")
def home():
    planets = query_db("""
        SELECT ID, Name, ImageURL FROM Planets;""")
    return render_template("home.html", planets=planets)

# Planet


@app.route("/planet/<int:id>")
def planet(id):
    sql = """
        SELECT * FROM Planets
        WHERE ID = ?;"""
    planet = query_db(sql, (id,), True)
    sql = """
        SELECT MoonID, Name, ImageURL FROM Moons
        WHERE PlanetID = ?;"""
    moons = query_db(sql, (id,), False)
    return render_template("planet.html", planet=planet, moons=moons)

# Moon


@app.route("/moon/<int:id>")
def moon(id):
    sql = """
        SELECT * FROM Moons
        WHERE MoonID = ?;"""
    moon = query_db(sql, (id,), True)
    return render_template("moon.html", moon=moon)

# Runner ##########################################


if __name__ == "__main__":
    app.run(debug=True)
