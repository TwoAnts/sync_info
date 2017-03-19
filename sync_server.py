#!/usr/bin/env python2
#-*- coding:utf-8 -*-

from flask import Flask, request
app = Flask(__name__)

DB_NAME = 'something.db'

import os, sqlite3
from datetime import datetime, date

CUR_DIR = os.path.abspath(os.path.dirname(__file__))

DB_PATH = os.path.join(CUR_DIR, DB_NAME)

CREATE_INFO_TABLE = 'create table if not exists info (\
id integer PRIMARY KEY,\
hostname text NOT NULL,\
ip text NOT NULL,\
time timestamp\
);'

def connect_db():
    return sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)

def init_db():
    conn = connect_db()
    conn.execute(CREATE_INFO_TABLE)
    conn.close()
   
init_db()


def save_info(hostname, ip):
    conn = connect_db()
    update_sql = 'insert or replace into info(id, hostname, ip, time) \
values( \
    (select id from info where hostname == ? and ip == ?),\
    ?, ?, ? );'

    info = [hostname, None, hostname, None, datetime.now()]
    if isinstance(ip, basestring):
        info[1] = ip
        info[3] = ip
        conn.execute(update_sql, info)
    else:
        for e in ip:
            info[1] = e
            info[3] = e
            conn.execute(update_sql, info)
    conn.commit()
    conn.close()

def query_info(hostname=''):
    query_sql = r'select hostname, ip, time from info '
    if hostname: query_sql += r'where hostname like ? ' 
    query_sql += ' order by hostname ASC, time DESC;'
    conn = connect_db()
    info = []
    param = (hostname, ) if hostname else ()
    for row in conn.execute(query_sql, param):
        info.append(row)
    conn.close()
    return info

template = \
'''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>sync_info</title>
</head>
<body>
    <table>
    %s
    </table>
</body>
</html>
'''
 
def dump_info(infos):
    strs = []
    for info in infos:
        strs.append('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' \
                            %(info[0], info[1], info[2]))
    r = '\n'.join(strs)
    return template %r

       

@app.route('/sync', methods=['GET'])
def sync_get_all():
    return dump_info(query_info())

@app.route('/sync/<hostname>', methods=['GET'])
def sync_get(hostname):
    return dump_info(query_info(hostname))
 
@app.route('/sync', methods=['POST'])
def sync_post():
    data = request.get_json(force=True)
    ips = data['ip']
    hostname = data['hostname']
    save_info(hostname, ips)
    return 'OK! :)'
       
#if __name__ == '__main__':
#    save_info('test', '0.0.0.0') 
#    print query_info()  
        

