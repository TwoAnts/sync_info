#!/usr/bin/env python2
#-*- coding:utf-8 -*-

from get_info import get_current_ip, get_hostname

import json
import urllib2
import sys
import logging
from logging.handlers import RotatingFileHandler
import traceback
import os

LOG_FILENAME = 'sync.log'
CUR_DIR = os.path.abspath(os.path.dirname(__file__))
LOG_FILEPATH = os.path.join(CUR_DIR, LOG_FILENAME)

logger = logging.getLogger('sync')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
                '%(asctime)s-%(name)s-%(levelname)s-%(message)s')
handler = RotatingFileHandler(LOG_FILEPATH, maxBytes=1024)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(logging.StreamHandler())


def sync(url):
    data = {}
    data['ip'] = get_current_ip()
    data['hostname'] = get_hostname()
    data = json.dumps(data).encode('utf-8')
    
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    try:
        resp = urllib2.urlopen(req)
    except:
        logger.info(traceback.format_exc())
        return False
    logger.info('%s %s %s' %(url, resp.getcode(), resp.read()))
    if resp.getcode() == 200:
        return True
    return False
    

    
    

if __name__ == '__main__':
    URL = "http://%s/sync" %sys.argv[1]
    sync(URL)
    


