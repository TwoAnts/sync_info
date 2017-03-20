#!/usr/bin/env python2
#-*- coding:utf-8 -*-

from get_info import get_current_ip, get_hostname

import json
import urllib2
import sys, os, time
import logging, traceback
from logging.handlers import RotatingFileHandler

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


def sync(url, try_times=3, try_delay=60):
    data = {}
    data['ip'] = get_current_ip()
    data['hostname'] = get_hostname()
    data = json.dumps(data).encode('utf-8')
    
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    times = 0
    except_msg = None
    while times < try_times:
        try:
            resp = urllib2.urlopen(req)
            logger.info('%s %s %s' %(url, resp.getcode(), resp.read()))
            if resp.getcode() == 200: return True
        except:
            except_msg = traceback.format_exc()
            times += 1 
        time.sleep(try_delay)
    if times >= try_times: logger.error(
                    'try %s time, but failed.\n%s' %(times, except_msg))
    return False
        

if __name__ == '__main__':
    URL = "http://%s/sync" %sys.argv[1]
    sync(URL)
    
