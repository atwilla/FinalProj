import math
import numpy as np

class KNNClassifier():

	def __init__(self, xTrain, yTrain, k=5):
		"""
		xTrain = 2D numpy array
		yTrain = 1D numpy array
		k = int
		"""
		self.xTrain = xTrain
		self.yTrain = yTrain
		self.k = int(k)
		self.classifications = []
		self.getClassifications()

	def getClassifications(self):

		for classification in self.yTrain:

			if classification not in self.classifications:
				self.classifications.append(classification)

	def addData(self, newX, newY):
		""" Append data to xTrain and yTrain """

		self.xTrain = np.concatenate((self.xTrain, newX))
		self.yTrain = np.concatenate((self.yTrain, newY))
		self.getClassifications()

	def clearData(self, newX=np.array([[]]), newY=np.array([])):
		""" Replace xTrain and yTrain with newX and newY. Resets original
		arrays by default"""

		self.xTrain = newX
		self.yTrain = newY

	def classify(self, x):
		""" Classify a given array of independent variables. Return a 1D numpy 
		array of the results. x must be a 2D numpy array of shape (n, 1)."""

		predictions = np.zeros(x.shape[0], self.yTrain.dtype)

		votes = {}

		# Calculate Euclidian distance from every test point to every training 
		# point.
		for i in range(x.shape[0]):
			distances = []

			for classification in self.classifications:
				votes[classification] = 0

			# Compare each test point to each training point.
			for j in range(self.xTrain.shape[0]):
				distance = 0

				# Calculate distance on each each axis.
				for k in range(self.xTrain[0].size):
					distance += (x[i][k] - self.xTrain[j][k]) ** 2

				distance = math.sqrt(distance)
				distances.append([distance, self.yTrain[j]])

			distances = sorted(distances, key=lambda elem: elem[0])

			for neighb in range(self.k):
				votes[distances[neighb][1]] += 1

			# Set prediction to highest voted type.
			predictions[i] = sorted(votes.items(), key=lambda vote: vote[1], reverse=True)[0][0]

		return np.array((predictions))
