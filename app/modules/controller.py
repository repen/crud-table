from modules.database import UserDB, \
        ErrorDataBaseGetRows, ErrorDataBaseGetRow, ErrorDataBaseUpdateRow, ErrorDataBaseDeleteRow
from pathlib import Path


parent = Path(__file__).parents[2]
PATH = str([x for x in parent.iterdir() if x.name == "app"][0].joinpath("{}" + ".db"))

class Methods:
    def __init__(self):
        self._methods = {}

    def add_method(self, func):
        self._methods[func.__name__] = func

    def get_method(self, name):
        return self._methods[name]

    def check_name_method(self, name):
        if name in self._methods:
            return True

def get_rows(params):
    db = UserDB(PATH.format(params["name_db"]))
    sql = "SELECT rowid, * FROM '{}'".format(params["name_table"])
    try:
        rows = db.get_rows(sql)
        return rows, 200
    except ErrorDataBaseGetRows:
        return {"Error": "Bad Request"}, 400

def update_row(params):
    db = UserDB(PATH.format(params["name_db"]))
    try:
        db.update_row(*UserDB.dict_row(params["name_table"],
                                   params["row"],
                                   mode = "update",
                                   rowid=params["row"]["rowid"]))
        return db.get_row("SELECT rowid, * FROM {} WHERE rowid = {}".format(params["name_table"],
                                params["row"]["rowid"])), 200
    except ErrorDataBaseUpdateRow:
        return {"Error": "Bad Request"}, 400

def insert_row(params):
    db = UserDB(PATH.format(params["name_db"]))
    try:
        db.update_row(*UserDB.dict_row(params["name_table"], params['row']))
        return db.get_row("SELECT rowid, * FROM {name} WHERE rowid = \
          (SELECT rowid FROM {name} ORDER BY rowid DESC)".format(name=params["name_table"])), 200
    except ErrorDataBaseUpdateRow:
        return {"Error": "Bad Request"}, 400

def delete_row(params):
    try:
        db = UserDB(PATH.format(params["name_db"]))
        row = params["row"]
        db.delete_row("DELETE FROM {} WHERE rowid = {} ".format(params["name_table"], row["rowid"]))
        return {"DELETE":"Successful"}, 200
    except ErrorDataBaseDeleteRow:
        return {"Error": "Bad Request"}, 400

def init_methods():
    methods = Methods()
    methods.add_method(get_rows)
    methods.add_method(insert_row)
    methods.add_method(update_row)
    methods.add_method(delete_row)
    return methods

def GET_controller(params):
    methods = init_methods()
    return methods.get_method(params["method"])(params)

def PUT_controller(params):
    methods = init_methods()
    return methods.get_method(params["method"])(params)

def POST_controller(params):
    methods = init_methods()
    return methods.get_method(params["method"])(params)

def DELETE_controller(params):
    methods = init_methods()
    return methods.get_method(params["method"])(params)

if __name__ == '__main__':
    pass