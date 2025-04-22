from flask import Flask, render_template
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

app.config.from_object(Config)
mysql = MySQL(app)
