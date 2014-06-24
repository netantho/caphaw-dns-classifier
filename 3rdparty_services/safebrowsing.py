import sys
import urllib

if __name__ == '__main__':
    if len(sys.argv) > 2:
        with file(sys.argv[1]) as f:
            apikey = sys.argv[2]
            for l in f.readlines():
            	domain = l[:-2]
            	url = urllib.urlopen('https://sb-ssl.google.com/safebrowsing/api/lookup?client=demo-app&apikey='+apikey+'&appver=1.5.2&pver=3.0&url=http://'+domain)
            	print '%s\t%s' % (domain, url.read())
    else:
        print "Usage: python safebrowsing.py <domains> <apikey>"
