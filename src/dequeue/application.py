# -*- coding: utf-8 -*-

import redis
import os
import re
import json
import constants

from apnsclient import *

# const
CERT_DIR = "apn_cert"
SANDBOX_PATTERN = '_sandbox$'

sandbox_re = re.compile(SANDBOX_PATTERN);

session = Session()

files = os.listdir(CERT_DIR);
app = {}
for filename in files:
    root, ext = os.path.splitext(filename)
    if ext == '.pem':
        cert = '%s/%s' % (CERT_DIR, filename)
        push_addr = 'push_production'
        if sandbox_re.match(filename):
            push_addr = 'push_sandbox'
        app[root] = {
            'cert': cert,
            'push_addr': push_addr,
#            'con' : session.get_connection(push_addr, cert_file=cert)
        }

print json.dumps(app)

r = redis.StrictRedis(host=constants.REDIS.HOST, port=constants.REDIS.PORT, db=0)
while 1:
    value = r.lpop(constants.REDIS.KEY)
    if value == None:
        break
    try:
        data = value.split(':', 4)
        if( !app.has_key(data[0]) ):
            break
        target = app[data[0]]
        
