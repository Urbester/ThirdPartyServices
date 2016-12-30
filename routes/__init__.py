# coding=utf-8
from accounts import *
from events import *

@app.route('/v1/', methods=["DELETE"])
def status():
    print request.data
    print "---------------------"
    print request.headers
    return '{\"Teste\": \"Já e agora?\"}'