from flask import Flask, render_template
import os
from modules.main import REST_crud_blueprint
from pathlib import Path, PurePath
import base64

app = Flask(__name__)
app.register_blueprint(REST_crud_blueprint)

DEV = os.getenv("APP_PATH", "")

def encode_js(path):
    base_dir = Path(__file__).parent
    js_file_path = PurePath(base_dir).joinpath(path)
    with open(str(js_file_path), "r", encoding="utf-8") as f:
        jsfile = f.read()
    jsfile = jsfile + "H"
    return base64.b64encode(jsfile.encode()).decode("utf-8")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/table-01")
def table_01():
    data = {"jsfile":encode_js("static/js/customers.js")}
    return render_template("table-01.html", data = data)

@app.route("/table-02")
def table_02():
    data = {"jsfile":encode_js("static/js/invoices.js")}
    return render_template("table-02.html", data = data)

@app.route("/table-03")
def table_03():
    data = {"jsfile":encode_js("static/js/tracks.js")}
    return render_template("table-03.html", data = data)

if __name__ == '__main__':
    if DEV:
        app.run()
    else:
        app.run(port=5003, host='0.0.0.0', debug=True)

