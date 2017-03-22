#!/usr/bin/env python2
#-*- coding:utf-8 -*-

from flask import Flask, request
app = Flask(__name__)

INFO_CLEAN_DAYS = 1

DB_NAME = 'something.db'

import os, sqlite3
from datetime import datetime, date, timedelta

CUR_DIR = os.path.abspath(os.path.dirname(__file__))

DB_PATH = os.path.join(CUR_DIR, DB_NAME)

CREATE_LOG_TABLE = 'create table if not exists log (\
id integet PRIMART KEY,\
action text NOT NULL,\
time timestamp NOT NULL\
);'

CREATE_INFO_TABLE = 'create table if not exists info (\
id integer PRIMARY KEY,\
hostname text NOT NULL,\
ip text NOT NULL,\
time timestamp NOT NULL\
);'

def connect_db():
    return sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)

def drop_table():
    conn = connect_db()
    conn.execute('drop table info;')
    conn.execute('drop table log;')
    conn.commit()
    conn.close()

def init_db():
    conn = connect_db()
    conn.execute(CREATE_LOG_TABLE)
    conn.execute(CREATE_INFO_TABLE)
    conn.close()
   
init_db()

def clean_info():
    conn = connect_db()
    clean_time_sql = 'select time from log where action == ?;'
    clean_sql = 'delete from info where time < ? and hostname in \
(select DISTINCT hostname from info where time >= ?);'
    update_clean_time_sql = 'insert or replace into log(id, action, time) \
values( (select id from log where action == ?), ?, ?);'
    cur = conn.execute(clean_time_sql, ('clean',))
    row = cur.fetchone()
    days = (datetime.now() - row[0]).days if row else -1
    if days >= 1 or days < 0:
        print 'clean info'
        deadtime = datetime.now() - timedelta(days=INFO_CLEAN_DAYS)
        conn.execute(clean_sql, (deadtime, deadtime))
        conn.execute(update_clean_time_sql, ('clean', 'clean', \
                                            datetime.now()))
        conn.commit()
        print 'clean info done. %s changed.' %conn.total_changes
        
    conn.close()
         

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
    total_changes = conn.total_changes
    conn.close()
    return total_changes

def query_info(hostname=''):
    clean_info()
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
    try:
        return dump_info(query_info())
    except:
        return 'Something crashed! :)'
    

@app.route('/sync/<hostname>', methods=['GET'])
def sync_get(hostname):
    try:
        return dump_info(query_info(hostname))
    except:
        return 'Something crashed! :)'
 
@app.route('/sync', methods=['POST'])
def sync_post():
    try:
        data = request.get_json(force=True)
        ips = data['ip']
        hostname = data['hostname']
        n = save_info(hostname, ips)
        return 'OK! :) (%s changed)' %n
    except:
        return 'Something crashed! :)'
       
#if __name__ == '__main__':
#    save_info('test', '0.0.0.0') 
#    print query_info()  
        

