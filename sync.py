#!/usr/bin/env python2
#-*- coding:utf-8 -*-

from get_info import get_current_ip, get_hostname

import json
import urllib2
import sys


def sync(url):
    data = {}
    data['ip'] = get_current_ip()
    data['hostname'] = get_hostname()
    data = json.dumps(data).encode('utf-8')
    
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    resp = urllib2.urlopen(req)
    print '%s %s %s' %(url, resp.getcode(), resp.read())
    if resp.getcode() == 200:
        return True
    return False
    

    
    

if __name__ == '__main__':
    URL = "http://%s/sync" %sys.argv[1]
    sync(URL)
    


