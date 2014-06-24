import sys
import json
import socket
import urllib

from parse import Parse

def dnsbh():
    f = file('domains.txt')
    domains = []
    for l in f.readlines():
        if l[0] == '#':
            # comment
            continue
        l = l.split('\t')
        domains.append(l[2])
    while 1:
        l = p.readline()
        if not l:
            break
        if l.fqdn in domains:
            print l.fqdn

def spamhaus():
    while 1:
        l = p.readline()
        if not l:
            break
        try:
            r = socket.gethostbyname(l.fqdn+'.dbl.spamhaus.org')
            print '%s\t%s' % (l.fqdn, r)
        except Exception as e:
            pass

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with file(sys.argv[1]) as f:
            p = Parse(f)
    else:
        print "Usage: python blacklists.py <dataset>"
