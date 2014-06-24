"""
Compute features
"""

import math
import re
import sys
from collections import Counter
import inspect

import numpy as np
from sklearn import preprocessing
import mlpy
import whois
from IPython import embed

from functools import wraps
import errno
import os
import signal

class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator

class Features(object):
    def __init__(self, p):
        self.p = p
        self.X = None
        self.X_scaled = None
        self.features_list = []

    def f01_dotsnumber(self, fqdn):
        """
        Number of dots in FQDN. Ex: toto.tata.com -> 2
        """
        return len(fqdn.split('.')) - 1

    def f03_occurrences(self, fqdn):
        """
        Number of occurences of the fqdn in the dataset
        """
        return self.p.occurrences[fqdn]

    def f04_length(self, fqdn):
        """
        Length of FQDN without the TLD. Ex: toto.com -> 4
        """
        return len(fqdn) - len(fqdn.split('.')[-1]) - 1

    def f06_entropy(self, fqdn):
        """
        Shannon entropy in FQDN without TLD and without dots: Ex: "1223334444" -> 1.8464393446710154

        Code snippet from http://rosettacode.org/wiki/Entropy#Python
        """
        # remove tld
        fqdn = '.'.join(fqdn.split('.')[:-1])
        # remove dots
        fqdn = fqdn.replace('.', '')
        p, lns = Counter(fqdn), float(len(fqdn))
        return -sum( count/lns * math.log(count/lns, 2) for count in p.values())

    def f07_includenumbers(self, fqdn):
        """
        FQDN includes numbers?
        """
        if re.search(r'[0-9]', fqdn):
            return 1
        return -1

    def f08_includehyphens(self, fqdn):
        """
        FQDN includes hyphen(s)?
        """
        if '-' in fqdn:
            return 1
        return -1

    def f09_vowelsper(self, fqdn):
        """
        Percentage of vowels in FQDN without TLD and dots
        """
        # remove tld
        fqdn = '.'.join(fqdn.split('.')[:-1])
        # remove dots
        fqdn = fqdn.replace('.', '')
        vowels = list("aeiouy")
        number_of_vowels = float(sum(fqdn.count(c) for c in vowels))
        return number_of_vowels / len(fqdn)

    def f10_includemedicdoctor(self, fqdn):
        """
        Include 'medic' or 'doctor' in FQDN?
        """
        if 'medic' in fqdn or 'doctor' in fqdn:
            return 1
        return -1

    def f11_includeship(self, fqdn):
        """
        Include 'ship' in FQDN?
        """
        if 'ship' in fqdn:
            return 1
        return -1

    def f12_includemail(self, fqdn):
        """
        Include 'mail' or 'smtp' in FQDN?
        """
        if 'mail' in fqdn or 'smtp' in fqdn:
            return 1
        return -1

    @timeout(5)
    def f13_whois_networksolutions(self, fqdn):
        """
        Registrar in whois == Network Solutions LLC if not a subdomain?
        """
        if len(fqdn.split('.')) - 1 == 1:
            try:
                if whois.query(fqdn) == 'NETWORK SOLUTIONS, LLC.':
                    return 1
                return -1
            except:
                return -1
        else:
            return -1

    def f14_tld_is_biz(self, fqdn):
        """
        TLD == .biz?
        """
        if fqdn.split('.')[-1] == 'biz':
            return 1
        return -1

    def f15_tld_is_cc(self, fqdn):
        """
        TLD == .cc?
        """
        if fqdn.split('.')[-1] == 'cc':
            return 1
        return -1

    def f16_tld_is_com(self, fqdn):
        """
        TLD == .com?
        """
        if fqdn.split('.')[-1] == 'com':
            return 1
        return -1

    def f17_tld_is_info(self, fqdn):
        """
        TLD == .info?
        """
        if fqdn.split('.')[-1] == 'info':
            return 1
        return -1

    def f18_tld_is_net(self, fqdn):
        """
        TLD == .net?
        """
        if fqdn.split('.')[-1] == 'net':
            return 1
        return -1

    def f19_tld_is_org(self, fqdn):
        """
        TLD == .org?
        """
        if fqdn.split('.')[-1] == 'org':
            return 1
        return -1

    def f20_tld_is_pw(self, fqdn):
        """
        TLD == .pw?
        """
        if fqdn.split('.')[-1] == 'pw':
            return 1
        return -1

    def f21_tld_is_ru(self, fqdn):
        """
        TLD == .ru?
        """
        if fqdn.split('.')[-1] == 'ru':
            return 1
        return -1

    def f22_tld_is_su(self, fqdn):
        """
        TLD == .su?
        """
        if fqdn.split('.')[-1] == 'su':
            return 1
        return -1

    def f23_includens(self, fqdn):
        """
        include ns[0-9] in FQDN?
        """
        if re.search(r'ns[0-9]', fqdn):
            return 1
        return -1

    def compute(self):
        for o in inspect.getmembers(self, predicate=inspect.ismethod):
            self.features_list.append(o[0])
        i = 0
        for fqdn in self.p.fqdn:
            # print fqdn, i, len(self.p.fqdn)
            sys.stdout.flush()
            features = [
                self.f01_dotsnumber(fqdn),
                self.f03_occurrences(fqdn),
                self.f04_length(fqdn),
                self.f06_entropy(fqdn),
                self.f07_includenumbers(fqdn),
                self.f08_includehyphens(fqdn),
                self.f09_vowelsper(fqdn),
                self.f10_includemedicdoctor(fqdn),
                self.f11_includeship(fqdn),
                self.f12_includemail(fqdn),
                self.f13_whois_networksolutions(fqdn),
                self.f14_tld_is_biz(fqdn),
                self.f15_tld_is_cc(fqdn),
                self.f16_tld_is_com(fqdn),
                self.f17_tld_is_info(fqdn),
                self.f18_tld_is_net(fqdn),
                self.f19_tld_is_org(fqdn),
                self.f20_tld_is_pw(fqdn),
                self.f21_tld_is_ru(fqdn),
                self.f22_tld_is_su(fqdn),
                self.f23_includens(fqdn)
            ]
            if self.X != None:
                self.X = np.append(self.X, [features], axis=0)
            else:
                self.X = np.array([features])
            i += 1

        # scale
        self.X_scaled = preprocessing.scale(self.X)

