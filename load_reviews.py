import sys, os
import pandas as pd
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sommelier.settings")

import django
django.setup()

from reviews.models import Review, Wine # importing models

def save_review_from_row(review_row):
	review = Review()
	review.id = review_row[0]
	review.user_name = review_row[1]
	review.wine = Wine.objects.get(id=review_row[2])
	review.rating = review_row[3]
	review.pub_date = datetime.datetime.now()
	review.comment = review_row[4]
	review.save()

if __name__ == "__main__":

	# check # of arguments
	if len(sys.argv) == 2:
		print ("Reading from file " + str(sys.argv[1]))
		# generating the data frame
		reviews_df = pd.read_csv(sys.argv[1])
		print (reviews_df)

		# apply save_review_from_row to each review (row) in data frame
		# uses review.models.Review to create a new instace from each row data
		reviews_df.apply(
			save_review_from_row,
			axis = 1 
		)

		print ("Loaded {} reviews into the DB".format(Review.objects.count()))

	else:

		print ("Please, provide a valid Reviews file path")