"""
Parse input file
"""

from collections import namedtuple

Line = namedtuple('Line', [
    'timestamp',
    'fqdn',
    'client_id',
    'qtype',
    'rcode',
    'geoip_lat',
    'geoip_long',
    'geoip_country'
])

class Parse(object):
    def __init__(self, fp):
        # string: file path
        self.fp = fp
        # occurence of FQDNs, {fqdn: number_of_occurences}
        self.occurrences = {}
        # list of FQDNs
        self.fqdn = []

    def readline(self):
        """
        Read file and return structure of the next line
        """
        with file(self.fp) as f:
            while 1:
                l = f.readline()
                if not l:
                    return None

                l = l.split('\t')
                return Line(
                    timestamp=float(l[0]),
                    fqdn=l[1][:-1],
                    client_id=l[2],
                    qtype=int(l[3]),
                    rcode=int(l[4]),
                    geoip_lat=float(l[5]),
                    geoip_long=float(l[6]),
                    geoip_country=l[7]
                )

    def compute_fqdn(self):
        """
        Parse FQDNs and compute numbers of occurences
        """
        with file(self.fp) as f:
            while 1:
                l = f.readline()
                if not l:
                    return None

                l = l.split('\t')
                fqdn = l[1][:-1]

                if fqdn in self.fqdn:
                    self.occurrences[fqdn] += 1
                else:
                    self.fqdn.append(l[1][:-1])
                    self.occurrences[fqdn] = 1
