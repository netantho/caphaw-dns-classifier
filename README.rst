This project is as classifier of DNS queries for an OpenDNS queries dataset_.
It aims at creating class of different FQDNs based on the activity of the FQDN, registration properties and filtering out noise.

.. _dataset: https://gist.github.com/jedisct1/a962e4aceab1f5aaf9da.

Usage
-----

Tested with Python 2.7.3 on Debian, within a virtualenv.

1. You need to install mlpy from the source because it's not available on pypi anymore.
2. $ pip install -r requirements.txt
3. $ python main.py ctest.out.txt

Preliminary findings
--------------------

Most of the domains are liked to the Caphaw [1] banking trojan.
Caphaw uses a lot of .su and .cc domains that are not very common in legitimate traffic [2].
It also uses random subdomains [6].

I used third party services to find more information about the domains:

* Google SafeBrowsing: nothing known, must have something to do with these domains forbidding indexation
* DNS-BH (malwaredomains.com): nothing known
* phishtank: nothing known
* spamhaus: 1/4 considered as spam, didn't really depends on the domain name syntax
* virustotal: interesting results for the malware-caphawinfra class
* urlquery.net (by hand): too bad it's really slow and they don't have an API yet
* malwr.com (by hand): too bad their API doesn't allow search

The scripts for third party services are in https://github.com/netantho/caphaw-dns-classifier/tree/master/3rdparty_services and the resuts in https://github.com/netantho/caphaw-dns-classifier/tree/master/3rdparty_results


Classes
-------

A big problem I had when trying to find classes is that almost all domains were already shut down.
Also, they were not indexed by Google.
So, I'm guessing a lot.

* malware-spamviagra: domains containing words such as 'medic' or 'doctor', usually sell viagra and other medecine [3][4][5]
* malware-caphawinfra: domains used by Caphaw, a lot of them are random subdomains, usually .su or .cc TLD
* legit-networksolutions: domains that are registered using Network Solutions LLC, most of them don't provide anything anymore or domain parking
* legit-mail: domains containing 'mail'
* legit-namecheap: domains with .pw TLD, registered using namecheap
* legit-dns: DNS servers

Features
--------

My features are only looking at the FQDN. Let me explain why first.
I used the timestamp info to identify the malware campaign. I don't have data on a timeline large enough in my opinion to use anomalies or recurrences in the time deltas. Plus, it's not very easy to filter out false positives related to this feature and it can be expensive to compute.
I used looked for number of client id per FQDN, it didn't really group queries in an interesting way (didn't match with 3rd party classifications at all).
The record type didn't have a lot of different values, mostly either A or AAAA queries. The AAAA queries didn't look to be based on the domain family.
In the response code we don't a lot of NXDOMAIN responses that would help identify DGA-based malware.
The GeoIP information of the client didn't display a specific trend for a specific country. It's a lot of Asian countries such as India or China but it's not surprising since the resolver is in Singapore. It would have been interesting to get the GeoIP information of the IP addresses linked to the domain names though.

The features I chose are as follow:

* f01_dotsnumber: Number of dots in FQDN. Ex: toto.tata.com -> 2
* f03_occurrences: Number of occurences of the fqdn in the dataset
* f04_length: Length of FQDN without the TLD. Ex: toto.com -> 4
* f06_entropy: Shannon entropy in FQDN without TLD and without dots: Ex: "1223334444" -> 1.8464393446710154
* f07_includenumbers: FQDN includes numbers?
* f08_includehyphens: FQDN includes hyphen(s)?
* f09_vowelsper: Percentage of vowels in FQDN without TLD and dots
* f10_includemedicdoctor: Include 'medic' or 'doctor' in FQDN?
* f11_includeship: Include 'ship' in FQDN?
* f12_includemail: Include 'mail' or 'smtp' in FQDN?
* f13_whois_networksolutions: Registrar in whois == Network Solutions LLC if not a subdomain?
* f14_tld_is_biz: TLD == .biz?
* f15_tld_is_cc: TLD == .cc?
* f16_tld_is_com: TLD == .com?
* f17_tld_is_info: TLD == .info?
* f18_tld_is_net: TLD == .net?
* f19_tld_is_org: TLD == .org?
* f20_tld_is_pw: TLD == .pw?
* f21_tld_is_ru: TLD == .ru?
* f22_tld_is_su: TLD == .su?
* f23_includens: include ns[0-9] in FQDN?

I 'scale' the features before using them (mean to 0, normalization).

Classification
--------------

I'm using a one-vs-all strategy.
I'm fitting one classifier per class (we have a multiclass problem here).
Each one of them uses a Linear Support Vector Classification.
I used these algorithms because they have a good result and complexity in most cases, and they are well-enough implemented in the python libraries that I use.

Web
---

I use flask (python microframework) as a web server and jinja2 for templating.
On the client side, I use bootstrap and jquery.


Future work
-----------

The classification is overfitting for this dataset. It would be better to make it more generic. I didn't really looked for performance in my code, it would also be something to improve.

For the interface, it would be cool to be able to see the details of the features (both scaled and not scaled) and to have a graph visualization of items based on the features they share.
I think it would be useful also to have a search and filtering features.

We probably want to find a better name for this project :).

References
----------

* [1] https://www.virustotal.com/en/file/92000067f4f07210eaaeaa6c4c024bc47b4624bb48a5728d315a895295e5cc79/analysis/
* [2] https://lists.emergingthreats.net/pipermail/emerging-sigs/2013-March/021626.html
* [3] http://pastebin.com/emiahiLM
* [4] http://urlquery.net/report.php?id=1397719095557
* [5] http://urlquery.net/report.php?id=1403381660529
* [6] http://www.welivesecurity.com/2013/02/25/caphaw-attacking-major-european-banks-with-webinject-plugin/
