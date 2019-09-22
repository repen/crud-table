# "SELECT sql FROM sqlite_master WHERE name ='Customers'"
import sqlite3
from pathlib import Path

class ErrorModulesInternal(Exception):
    pass

class ErrorDataBaseGetRows(ErrorModulesInternal):
    pass

class ErrorDataBaseGetRow(ErrorModulesInternal):
    pass

class ErrorDataBaseUpdateRow(ErrorModulesInternal):
    pass

class ErrorDataBaseDeleteRow(ErrorModulesInternal):
    pass

parent = Path(__file__).parents[2]
PATH = str([x for x in parent.iterdir() if x.name == "app"][0].joinpath("{}" + ".db"))

class UserDB:

    @staticmethod
    def dict_row(tablename, args, mode="insert", rowid=None):
        if mode == "insert":
            keys = ','.join(args.keys())
            values_marks = ','.join(list('?' * len(args)))
            values = [tuple(args.values())]
            sql = 'INSERT INTO ' + tablename + ' (' + keys + ') VALUES (' + values_marks + ')'
        if mode == "update":
            string, values = '', []
            for k, v in zip(args.keys(), args.values()):
                string += "{} = ?, ".format(k)
                values.append(v)
            sql = 'UPDATE ' + tablename + ' SET ' + string[:-2] + ' WHERE rowid = {}'.format(rowid)
            values = [tuple(values)]
        return [sql, values]

    def __init__(self, path):
        self.path = path

    def connect(self):
        return sqlite3.connect(self.path)

    def dict_factory(self,cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def get_rows(self, sql, row = True, encoding=False):
        try:
            conn = self.connect()
            if encoding:
                conn.text_factory = lambda x: str(x, 'latin1')
            if row:
                # conn.row_factory = sqlite3.Row
                conn.row_factory = self.dict_factory
            cursor = conn.cursor()
            cursor.execute(sql)
            res = cursor.fetchall()
            return res
        except sqlite3.Error as e:
            raise ErrorDataBaseGetRows("[Error GET ROWS] [Operation SELECT not runned]") from e
        finally:
            conn.close()

    def get_row(self, sql, row = True, encoding=False):
        try:
            conn = self.connect()
            if encoding:
                conn.text_factory = lambda x: str(x, 'latin1')
            if row:
                conn.row_factory = self.dict_factory
            cursor = conn.cursor()
            cursor.execute(sql)
            res = cursor.fetchone()
            return res
        except sqlite3.Error as e:
            raise ErrorDataBaseGetRow("[Error GET ROW] [Operation SELECT not runned]") from e
        finally:
            conn.close()


    def update_row(self, sql, args):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.executemany(sql, args)
            conn.commit()
        except sqlite3.Error as e:
            raise ErrorDataBaseUpdateRow("[Error UPDATE ROW] [Operation update not runned]") from e
        finally:
            conn.close()

    def delete_row(self, sql):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
        except sqlite3.Error as e:
            raise ErrorDataBaseDeleteRow("[Error DELETE ROW] [Operation delete not runned]") from e
        finally:
            conn.close()

if __name__ == '__main__':
    db = UserDB(PATH.format("chinook"))
    # res = db.get_rows("SELECT name FROM sqlite_master WHERE type = 'table'", row = False)
    # res = db.get_rows("SELECT sql, name FROM sqlite_master WHERE name = 'customers'", row = True)
    res = db.get_rows("SELECT rowid, * FROM tracks", row = True)
    print(res)



# [('albums',), ('sqlite_sequence',), ('artists',), ('customers',), ('employees',), ('genres',), 
# ('invoices',), ('invoice_items',), ('media_types',), ('playlists',), ('playlist_track',), 
# ('tracks',), ('sqlite_stat1',)]