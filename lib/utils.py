def return_http_msg(http_code, message=None, token=None, rest=True):
    from flask import make_response
    from json import dumps

    resp = make_response()
    resp.header = {}
    resp.status_code = http_code
    if token is not None:
        resp.header.update({"X-Auth-Token": token})
    if rest:
        resp.header.update({"Content-type": "application/json"})
        resp.header.update({"Accept": "application/json"})
    resp.status_code = http_code
    if http_code >= 400:
        resp.data = dumps({"Reason": message})
    else:
        resp.data = dumps({"Result": message})
    return resp