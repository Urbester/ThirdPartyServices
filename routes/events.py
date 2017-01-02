from flask import request

from application import app
from beans import AccountBean
from beans import EventBean
from models import User, Event
from lib.utils import return_http_msg

    ###########################
    # EVENT CREATION/DELETION #
    ###########################

# METHOD FOR CREATING EVENT
@app.route('/v1/event', methods=["POST"])
def create_event():
    data = request.get_json()
    if not set(
            ["Title", "Description", "StartDate", "EndDate", "Local", "Price", "Public", "MaxGuests", "URL"]).issubset(
        data.keys()):
        return return_http_msg(400,
                               message="Expected Title, StartDate, EndDate, Local, Description, Price, Public, maxGuests, URL")
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")

    owner = AccountBean()
    if not owner.get_account(request.headers["X-Auth-Token"]):
        return return_http_msg(400, message="Invalid AccessToken")
    bean = EventBean()

    if data["Public"] == "true":
        data["Public"] = True
    else:
        data["Public"] = False

    host = User.query.filter_by(accessToken=request.headers["X-Auth-Token"]).first()
    if bean.new_event(data["Title"],
                      data["StartDate"],
                      data["EndDate"],
                      data["Local"],
                      data["Description"],
                      data["Price"],
                      host.id,
                      data["Public"],
                      data["MaxGuests"],
                      data["URL"]):
        return return_http_msg(200, message=bean.result)
    else:
        return return_http_msg(400, message=bean.result)


# METHOD TO RETRIEVE INFORMATION ABOUT EVENT
@app.route('/v1/event', methods=["GET"])
def get_event():
    # X-Auth-Token Needed
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")
    bean = EventBean()
    event_id = request.args.get('id')
    if bean.get_event(id=event_id, token=request.headers["X-Auth-Token"]):
        return return_http_msg(200, message=bean.result)
    else:
        return return_http_msg(400, message=bean.result)


# METHOD FOR HOST TO DELETE AN EVENT
@app.route('/v1/event', methods=["DELETE"])
def delete_event():
    # X-Auth-Token Needed
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")
    user = User.query.filter_by(accessToken=request.headers["X-Auth-Token"]).first()
    bean = EventBean()
    data = request.get_json()
    if bean.delete_event(id=data["Id"], host=user):
        return return_http_msg(200, message=bean.result)
    else:
        return return_http_msg(400, message=bean.result)


# NICE TO HAVE FEATURE - UNTESTED
@app.route('/v1/event', methods=["PUT"])
def update_event():
    if ["Id", "Title", "StartDate", "EndDate", "Local", "Description", "Price"] not in request.data:
        return return_http_msg(400, message="Expected Id, Title, StartDate, EndDate, Local, Description, Price")
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")
    owner = User.query.filter_by(accessToken=request.data["X-Auth-Token"])
    bean = EventBean()
    if bean.update_event(request.data["Id"], request.data["Title"], request.data["StartDate"], request.data["EndDate"],
                         request.data["Local"], request.data["Description"], request.data["Price"],
                         owner):
        return return_http_msg(200, message=bean.result)
    else:
        return return_http_msg(400, message=bean.result)

        ##################
        # MANAGING SLOTS #
        ##################

# USER METHODS FOR ACCEPTING/REJECTING INVITES TO PRIVATE PARTIES
@app.route('/v1/event/accept', methods=['GET'])
def accept_event():
    event_id = request.args.get('id')
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")
    user = User.query.filter_by(accessToken=request.headers["X-Auth-Token"]).first()
    bean = EventBean()
    if bean.accept_event(event_id, user):
        return return_http_msg(200, message=bean.result)
    else:
        return return_http_msg(400, message=bean.result)


# METHOD FOR USER TO REJECT AN INVITATION
@app.route('/v1/event/reject', methods=['GET'])
def reject_event():
    event_id = request.args.get('id')
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")
    user = User.query.filter_by(accessToken=request.headers["X-Auth-Token"]).first()
    bean = EventBean()
    if bean.reject_event(event_id, user):
        return return_http_msg(200, message=bean.result)
    else:
        return return_http_msg(400, message=bean.result)


# METHOD FOR OWNER TO ACCEPT PENDING USERS
@app.route('/v1/event/list/pending', methods=['POST'])
def accept_pending_user():
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")
    data = request.get_json()
    event_id = data["Id"]
    user_email = data["Email"]
    owner = User.query.filter_by(accessToken=request.headers["X-Auth-Token"]).first()
    bean = EventBean()
    if bean.accept_pending(user_email, event_id, owner):
        return return_http_msg(200, message=bean.result)
    else:
        return return_http_msg(400, message=bean.result)


# METHOD FOR OWNER TO REJECT PENDING USERS
@app.route('/v1/event/list/pending', methods=['DELETE'])
def reject_pending_user():
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")
    data = request.get_json()
    event_id = data["Id"]
    user_email = data["Email"]
    owner = User.query.filter_by(accessToken=request.headers["X-Auth-Token"]).first()
    bean = EventBean()
    if bean.reject_pending(user_email, event_id, owner):
        return return_http_msg(200, message=bean.result)
    else:
        return return_http_msg(400, message=bean.result)


# METHOD FOR OWNER TO INVITE USERS
@app.route('/v1/event/invite', methods=['POST'])
def invite_to_event():
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")
    owner = User.query.filter_by(accessToken=request.headers["X-Auth-Token"]).first()
    data = request.get_json()
    user_email = data["user_email"]
    event_id = data["event_id"]
    bean = EventBean()
    if bean.invite_users(user_email, event_id, owner):
        return return_http_msg(200, message=bean.result)
    else:
        return return_http_msg(400, message=bean.result)


# METHOD FOR ASKING TO JOIN PUBLIC PARTY
@app.route('/v1/event/ask', methods=['GET'])
def ask_to_join_party():
    event_id = request.args.get('id')
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")
    user = User.query.filter_by(accessToken=request.headers["X-Auth-Token"]).first()
    bean = EventBean()
    if bean.ask_to_join_event(event_id, user):
        return return_http_msg(200, message=bean.result)
    else:
        return return_http_msg(400, message=bean.result)


        ###############
        # EVENT LISTS #
        ###############


# GET PUBLIC EVENT LIST
@app.route('/v1/event/list/public', methods=["GET"])
def get_event_lists():
    # X-Auth-Token Needed
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")
    bean = AccountBean()
    if bean.get_account(accessToken=request.headers["X-Auth-Token"]):
        event = EventBean()
        user = User.query.filter_by(accessToken=bean.result["accessToken"]).first()
        event.get_event_list(user)
        return return_http_msg(200, message=event.result)
    else:
        return return_http_msg(400, message=bean.result)


# GET HOSTING EVENTS
@app.route('/v1/event/list/hosting', methods=['GET'])
def get_hosting_event_lists():
    # X-Auth-Token Needed
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")
    bean = AccountBean()
    if bean.get_account(accessToken=request.headers["X-Auth-Token"]):
        event = EventBean()
        user = User.query.filter_by(accessToken=bean.result["accessToken"]).first()
        event.get_hosting_event_list(user)
        return return_http_msg(200, message=event.result)
    else:
        return return_http_msg(400, message=bean.result)


# GET ACCEPTED EVENTS
@app.route('/v1/event/list/accepted', methods=['GET'])
def get_accepted_event_lists():
    # X-Auth-Token Needed
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")
    bean = AccountBean()
    if bean.get_account(accessToken=request.headers["X-Auth-Token"]):
        event = EventBean()
        user = User.query.filter_by(accessToken=bean.result["accessToken"]).first()
        event.get_accepted_event_list(user)
        return return_http_msg(200, message=event.result)
    else:
        return return_http_msg(400, message=bean.result)


# GET REJECTED EVENTS
@app.route('/v1/event/list/rejected', methods=['GET'])
def get_rejected_event_lists():
    # X-Auth-Token Needed
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")
    bean = AccountBean()
    if bean.get_account(accessToken=request.headers["X-Auth-Token"]):
        event = EventBean()
        user = User.query.filter_by(accessToken=bean.result["accessToken"]).first()
        event.get_rejected_event_list(user)
        return return_http_msg(200, message=event.result)
    else:
        return return_http_msg(400, message=bean.result)


# GET PENDING EVENTS
@app.route('/v1/event/list/pending', methods=['GET'])
def get_pending_event_lists():
    # X-Auth-Token Needed
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")
    bean = AccountBean()
    if bean.get_account(accessToken=request.headers["X-Auth-Token"]):
        event = EventBean()
        user = User.query.filter_by(accessToken=bean.result["accessToken"]).first()
        event.get_pending_event_list(user)
        return return_http_msg(200, message=event.result)
    else:
        return return_http_msg(400, message=bean.result)


# GET INVITED EVENTS
@app.route('/v1/event/list/invited', methods=['GET'])
def get_invited_event_lists():
    # X-Auth-Token Needed
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")
    bean = AccountBean()
    if bean.get_account(accessToken=request.headers["X-Auth-Token"]):
        event = EventBean()
        user = User.query.filter_by(accessToken=bean.result["accessToken"]).first()
        event.get_invited_event_list(user)
        return return_http_msg(200, message=event.result)
    else:
        return return_http_msg(400, message=bean.result)


# GET UPCOMING EVENTS
@app.route('/v1/event/list/upcoming', methods=['GET'])
def get_upcoming_events():
    # X-Auth-Token Needed
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")
    bean = AccountBean()
    if bean.get_account(accessToken=request.headers["X-Auth-Token"]):
        event = EventBean()
        user = User.query.filter_by(accessToken=bean.result["accessToken"]).first()
        event.get_upcoming_events(user)
        return return_http_msg(200, message=event.result)
    else:
        return return_http_msg(400, message=bean.result)

        ###############
        # USERS LISTS #
        ###############


# GET ALL USER LISTS OF EVENT
@app.route('/v1/event/list', methods=['GET'])
def get_users_list():
    # X-Auth-Token Needed
    event_id = request.args.get('id')
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")
    bean = AccountBean()
    if bean.get_account(accessToken=request.headers["X-Auth-Token"]):
        event = EventBean()
        event.get_user_lists(event_id)
        return return_http_msg(200, message=event.result)
    else:
        return return_http_msg(400, message=bean.result)


# GET ALL AVAILABLE USERS FOR EVENT
@app.route('/v1/event/available', methods=['GET'])
def det_available_users():
    # X-Auth-Token Needed
    event_id = request.args.get('id')
    if "X-Auth-Token" not in request.headers:
        return return_http_msg(400, message="X-Auth-Token required.")
    bean = AccountBean()
    if bean.get_account(accessToken=request.headers["X-Auth-Token"]):
        event = EventBean()
        event.get_available_users(event_id)
        return return_http_msg(200, message=event.result)
    else:
        return return_http_msg(400, message=bean.result)
