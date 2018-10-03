from .models import Review, Wine, Cluster
from django.contrib.auth.models import User
from sklearn.cluster import KMeans
from scipy.sparse import dok_matrix, csr_matrix
import numpy as np
import pandas as pd
from numba import jit

def update_clusters():
	num_reviews = Review.objects.count()
	update_step = ((num_reviews/100)+1) * 5
	if num_reviews % update_step == 0: # magic numbers zzzz
		"""
		# Generating a sparse matrix from user reviews
		#
		# User x Wine matrix: i,j: rating for wine j by user i
		"""
		# list of users
		users = [obj.username for obj in User.objects.only("username")]
		# set of all reviewed wines
		wine_ids = set([obj.wine.id for obj in Review.objects.only("wine")])
		# generate a dok_matrix (dictionary of keys based sparse matrix)
		ratings_matrix = dok_matrix((len(users), max(wine_ids)+1), dtype=np.float32)
		# populating matrix
		for i,v in enumerate(users): # for each user
			# generate a list of reviews by the user
			user_reviews = Review.objects.filter(user_name=v)
			for review in user_reviews: # for each review
				# add rating for the corresponding wine id in the matrix
				ratings_matrix[i,review.wine.id] = review.rating
		"""
		# Kmeans Clustering
		#
		# just forces 2 or more clusters. Needs to be revamped for a production grade implementation
		"""
		k = len(users) // 10 + 2 # based on # of users. 
		kmeans = KMeans(n_clusters=k)
		# fitting matrix with K Means
		# converting the dok_matrix to a csr_matrix for added efficiency
		clustering = kmeans.fit(ratings_matrix.tocsr())

		"""
		# Update clusters
		"""
		Cluster.object.all().delete() # deleting all previous clusters
		# generating a dictionary (hashmap) of clusters (k clusters from Kmeans above)
		new_clusters = {i: Cluster(name=i) for i in range(k)}
		# saving (pushing) each cluster to DB
		for cluster in new_clusters.values():
			cluster.save()
		# adding users to each cluster
		for i,v in enumerate(clustering.labels_):
			new_clusters[v].users.add(User.objects.get(username=users[i]))


