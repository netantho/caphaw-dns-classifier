import sys
import urllib
import json
import time

if __name__ == '__main__':
    if len(sys.argv) > 2:
        with file(sys.argv[1]) as f:
            apikey = sys.argv[2]
            results = []
            i = 1
            for l in f.readlines():
                if i % 4 == 0:
                    print 'sleeping'
                    sys.stdout.flush()
                    time.sleep(61)
                    print 'waking up'
                    sys.stdout.flush()
            	domain = l[:-2]
                url = 'https://www.virustotal.com/vtapi/v2/domain/report'
                parameters = {'domain': domain, 'apikey': apikey}
                response = urllib.urlopen('%s?%s' % (url, urllib.urlencode(parameters))).read()
                print domain
                try:
                    response_dict = json.loads(response)
                    results.append(response_dict)
                    print response_dict
                    sys.stdout.flush()
                except:
                    print "JSON encoding error: %s" % response
                    sys.stdout.flush()
                #i+=1
            print json.dumps(results)
    else:
        print "Usage: python virustotal.py <domains> <apikey>"
