"""
Main module
Launch program and web server
"""

import sys
from flask import Flask, render_template

from parse import Parse
from features import Features
from classification import Classification

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print 'Parsing...',
        sys.stdout.flush()
        p = Parse(sys.argv[1])
        p.compute_fqdn()
        print 'DONE'

        print 'Computing features (Can take some time because of whois queries)...',
        sys.stdout.flush()
        features = Features(p)
        features.compute()
        print 'DONE'

        print 'Classification...',
        sys.stdout.flush()
        classification = Classification(features, p)
        classification.compute()
        print 'DONE'

        print 'Launching webserver...',
        sys.stdout.flush()
        flask_app = Flask('caphaw-dns-classifier')
        print 'DONE'

        @flask_app.route('/')
        def index():
            return render_template('index.html',
                X=features.X,
                X_scaled=features.X_scaled,
                features_list=[features.features_list]*len(features.X_scaled),
                all=sorted(classification.all),
                classes=classification.classes,
                occurrences=p.occurrences,
                zip=zip(features.features_list, features.X, features.X_scaled))

        print "READY, Open http://%s:%d in your browser" % ('192.168.57.7', 8080)
        flask_app.run(host='192.168.57.7', port=8080, debug=False)
    else:
        print 'Usage: python main.py <dataset>'
        sys.exit()
