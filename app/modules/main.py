from flask import Blueprint, request, jsonify
from modules.controller import GET_controller, PUT_controller, POST_controller, DELETE_controller
class ErrorRestDataExternal(Exception):
    pass

REST_crud_blueprint = Blueprint('rest.crud', __name__)

def check_param(db, table):
    # allow, res = {"car": "automobile", "dealer": "dealers"}, False
    allow, res = [{"chinook": "Customers"}, {"chinook": "invoices"}, {"chinook":"tracks"}], False
    for al in allow:
        if db in al.keys() and table in al.values():
            res = True; break
    return res

@REST_crud_blueprint.route("/crud/<string:database>/<string:table>", methods=["GET"])
def get_rows(database, table):
    try:
        if not check_param(database, table):
            raise ErrorRestDataExternal("[GET] [ Error parameters]")

        if not request.args.get("method", False):
            raise ErrorRestDataExternal("[GET] [ Error method ]")

        if request.args.get("method") != get_rows.__name__:
            raise ErrorRestDataExternal("[GET] [ Error method ]")

        params = {"name_db": database, "name_table": table, 'method':  request.args.get("method")}
        response = GET_controller(params)
        return jsonify(response[0]), response[1]
    except ErrorRestDataExternal as e:
        return jsonify({"Error": str(e)}), 400


@REST_crud_blueprint.route("/crud/<string:database>/<string:table>", methods=["PUT"])
def update_row(database, table):
    try:
        if not check_param(database, table):
            raise ErrorRestDataExternal("[PUT] [ Error parameters]")

        params = {"name_db": database, "name_table":table, 'row': request.form.to_dict(),
                  "method": update_row.__name__}
        response = PUT_controller(params)
        return jsonify(response[0]), response[-1]
    except ErrorRestDataExternal as e:
        return jsonify({"Error": str(e)}), 400


@REST_crud_blueprint.route("/crud/<string:database>/<string:table>", methods=["POST"])
def insert_row(database, table):
    try:
        if not check_param(database, table):
            raise ErrorRestDataExternal("[POST] [ Error parameters]")

        params = {"name_db": database, "name_table": table, 'row': request.form.to_dict(),
                  "method":insert_row.__name__}
        response = POST_controller(params)
        return jsonify(response[0]), response[-1]
    except ErrorRestDataExternal as e:
        return jsonify({"Error": str(e)}), 400

@REST_crud_blueprint.route("/crud/<string:database>/<string:table>", methods=["DELETE"])
def delete_row(database, table):
    try:
        if not check_param(database, table):
            raise ErrorRestDataExternal("[DELETE] [ Error parameters]")

        params = {"name_db": database, "name_table": table, 'row': request.form.to_dict(),
                  "method":delete_row.__name__}
        response = DELETE_controller(params)
        return jsonify(response[0]), response[-1]
    except ErrorRestDataExternal as e:
        return jsonify({"Error": str(e)}), 400