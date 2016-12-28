from flask import request

from application import app
from beans import AccountBean
from lib.utils import return_http_msg


@app.route('/v1/account/', methods=["GET"])
def get_account_info():
    # X-Auth-Token Needed
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")
    bean = AccountBean()
    if bean.get_account(accessToken=request.headers["X-Auth-Token"]):
        return return_http_msg(200, message=bean.result)
    else:
        return return_http_msg(400, message=bean.result)


@app.route('/v1/account/', methods=["POST"])
def create_account():
    if ["AccessToken", "Name", "Email"] not in request.data:
        return return_http_msg(400, message="AccessToken, Name and Email required.")
    bean = AccountBean()
    if bean.new_account(request.data["Name"], request.data["AccessToken"], request.data["Email"]):
        return return_http_msg(200, message=bean.result)
    else:
        return return_http_msg(400, message=bean.result)


@app.route('/v1/account', methods=["DELETE"])
def delete_account():
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")
    bean = AccountBean()
    if bean.delete_account(accessToken=request.headers["X-Auth-Token"]):
        return return_http_msg(200, message=bean.result)
    else:
        return return_http_msg(400, message=bean.result)
