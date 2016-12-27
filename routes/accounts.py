from flask import request

from application import app
from lib.utils import return_http_msg


@app.route('/v1/account', methods=["GET"])
def get_account_info():
    # X-Auth-Token Needed
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")
    return return_http_msg(200, message=info)


@app.route('/v1/account', methods=["POST"])
def create_account():
    return return_http_msg(200, message="Account created with success.")


@app.route('/v1/account', methods=["DELETE"])
def delete_account():
    return return_http_msg(200, message="Account deleted with success.")
