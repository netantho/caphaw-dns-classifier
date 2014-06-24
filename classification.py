"""
Perform the classification based on features
"""

from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from IPython import embed


class Classification(object):
	def __init__(self, features, p):
		self.p = p
		self.features = features
		# {className: [item1, item2,...]}
		self.classes = {}
		# [number: name]
		self.labels = []
		self.training = ([], [])
		self.all = []
		self.classifier = None

	def learning(self, fp='training.txt'):
		f = file(fp)
		for l in f.readlines():
			l = l.split('\t')
			if l[1] not in self.labels:
				self.labels.append(l[1][:-1])
			label = self.labels.index(l[1][:-1])
			fqdn_id = self.p.fqdn.index(l[0])
			self.training[0].append(self.features.X_scaled[fqdn_id])
			self.training[1].append(label)
		f.close()
		self.classifier = OneVsRestClassifier(LinearSVC(random_state=0)).fit(self.training[0], self.training[1])

	def compute(self):
		self.learning()
		result = self.classifier.predict(self.features.X_scaled)
		fqdn_id = 0
		for i in result:
			if self.classes.has_key(self.labels[i]):
				self.classes[self.labels[i]].append(self.p.fqdn[fqdn_id])
			else:
				self.classes[self.labels[i]] = [self.p.fqdn[fqdn_id]]
			self.all.append(self.p.fqdn[fqdn_id])
			fqdn_id += 1

		for classname in self.classes.keys():
			self.classes[classname] = sorted(self.classes[classname])

		# embed()

