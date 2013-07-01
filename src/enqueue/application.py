# -*- coding: utf-8 -*-
from flask import Flask, request, Response

import constants
import redis
import json
import logging

app = Flask(__name__)
app.config.from_object('config')

@app.route("/")
def check():
    ret = { 'status':'ok' }
    return Response(json.dumps(ret), status=200, mimetype='application/json')

@app.route("/enqueue", methods=['POST'])
def enqueue():
    data = json.loads(request.data)
    pns = data['pns']
    enqueue = 0
    error   = 0
    r = redis.StrictRedis(host=constants.REDIS.HOST, port=constants.REDIS.PORT, db=0)
    for pn in pns:
        try:
            app          = pn['app']
            device_type  = pn['type']
            device_token = pn['token']
            budge_number = pn['badge']
            text         = pn['text']
            r.rpush(constants.REDIS.KEY,'%s:%s:%s:%d:%s' % (app,device_type,device_token, budge_number, text))
            enqueue = enqueue + 1
        except Exception,e:
            logging.error(e)
            error = error + 1
    ret = {
        'enqueue': enqueue,
        'error': error,
    }
    return Response(json.dumps(ret), status=201, mimetype='application/json')

if __name__ == "__main__":
    app.run()
