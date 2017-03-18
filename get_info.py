#!/usr/bin/env python2
#-*- coding:utf-8 -*-

import netifaces  
def get_current_ip():  
    ''''' 
    Using netifaces to fetch the ip address of the current machine. 
    '''  
    ips = []  
    exclude_iface = ['lo']  
    interfaces = netifaces.interfaces()  
    for iface in interfaces:  
        if iface not in exclude_iface:  
            if netifaces.AF_INET in netifaces.ifaddresses(iface):  
                addrs = netifaces.ifaddresses(iface)[netifaces.AF_INET] # mac addr: netifaces.AF_LINK  
                for addr in addrs:
                    ips.append(addr['addr'])
    return ips  

import socket
def get_hostname():
    return socket.gethostname()
  
if __name__ == '__main__':
    ips = get_current_ip()  
    print ips  
