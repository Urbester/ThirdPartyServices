from flask import request

from application import app
from beans import EventBean
from models import User
from lib.utils import return_http_msg


@app.route('/v1/event', methods=["POST"])
def create_event():
    if ["Id", "Title", "StartDate", "EndDate", "Local", "Description", "Price"] not in request.data:
        return return_http_msg(400, message="Expected Id, Title, StartDate, EndDate, Local, Description, Price")
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")
    owner = User.query.filter_by(accessToken=request.data["X-Auth-Token"])
    bean = EventBean()
    if bean.new_event(request.data["Title"], request.data["StartDate"], request.data["EndDate"],
                      request.data["Local"], request.data["Description"], request.data["Price"],owner):
        return return_http_msg(200, message=bean.result)
    else:
        return return_http_msg(400, message=bean.result)


@app.route('/v1/event', methods=["GET"])
def get_event():
    # X-Auth-Token Needed
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")
    bean = EventBean()
    if bean.get_event(id=request.data["Id"]):
        return return_http_msg(200, message=bean.result)
    else:
        return return_http_msg(400, message=bean.result)


@app.route('/v1/event', methods=["DELETE"])
def delete_event():
    # X-Auth-Token Needed
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")
    owner = User.query.filter_by(accessToken=request.data["X-Auth-Token"])
    bean = EventBean()
    if bean.delete_event(id=request.data["Id"],owner=owner):
        return return_http_msg(200, message=bean.result)
    else:
        return return_http_msg(400, message=bean.result)


@app.route('/v1/event', methods=["PUT"])
def update_event():
    if ["Id", "Title", "StartDate", "EndDate", "Local", "Description", "Price"] not in request.data:
        return return_http_msg(400, message="Expected Id, Title, StartDate, EndDate, Local, Description, Price")
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")
    owner = User.query.filter_by(accessToken=request.data["X-Auth-Token"])
    bean = EventBean()
    if bean.update_event(request.data["Id"],request.data["Title"], request.data["StartDate"], request.data["EndDate"],
                         request.data["Local"], request.data["Description"], request.data["Price"],
                         owner):
        return return_http_msg(200, message=bean.result)
    else:
        return return_http_msg(400, message=bean.result)
