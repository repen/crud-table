from flask import Flask, render_template
import os
from modules.main import REST_crud_blueprint


app = Flask(__name__)
app.register_blueprint(REST_crud_blueprint)

DEV = os.getenv("APP_PATH", "")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/table-01")
def table_01():
    return render_template("table-01.html")

@app.route("/table-02")
def table_02():
    return render_template("table-02.html")

@app.route("/table-03")
def table_03():
    return render_template("table-03.html")

if __name__ == '__main__':
    if DEV:
        app.run()
    else:
        app.run(port=5003, host='0.0.0.0', debug=True)

