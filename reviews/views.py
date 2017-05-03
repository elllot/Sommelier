from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Review, Wine, Cluster
from .forms import ReviewForm, WineForm
from .suggestions import update_clusters
from django.contrib.auth.models import User
import datetime

from django.contrib.auth.decorators import login_required
# Create your views here.

# view to list all reviews 
def review_list(request):
	latest_review_list = Review.objects.order_by('-pub_date')[:9]
	context = {'latest_review_list':latest_review_list}
	return render(request, 'reviews/review_list.html', context)

# view to show review details of a wine
def review_detail(request, review_id):
	# review object where PK is equal to the review_id
	review = get_object_or_404(Review, pk=review_id)
	# render function
	return render(request, 'reviews/review_detail.html', {'review': review})

# view for fetching list of all wines from the DB
def wine_list(request):
	wine_list = Wine.objects.order_by('-name')
	context = {'wine_list': wine_list}
	return render(request, 'reviews/wine_list.html', context)

# view for listing the details of a given wine
def wine_detail(request, wine_id):
	wine = get_object_or_404(Wine, pk=wine_id)
	form = ReviewForm()
	return render(request, 'reviews/wine_detail.html', {'wine': wine, 'form': form})

# view that contains the form for adding a wine
def wine_add(request):
	form = WineForm()
	return render(request, 'reviews/wine_add.html', {'form': form})

# list of reviews 
def user_review_list(request, username=None):
	if not username:
		username = request.user.username
	latest_reviews = Review.objects.filter(user_name=username).order_by('-pub_date')
	context = {'latest_review_list': latest_reviews, 'username':username}
	return render(request, 'reviews/user_review_list.html', context)

# view for querying and adding a review to the DB
@login_required
def add_review(request, wine_id):
	wine = get_object_or_404(Wine, pk=wine_id)
	form = ReviewForm(request.POST)
	if form.is_valid():
		rating = form.cleaned_data['rating']
		comment = form.cleaned_data['comment']
		user_name = request.user.username
		review = Review()
		review.user_name = user_name
		review.wine = wine
		review.rating = rating
		review.comment = comment
		review.pub_date = datetime.datetime.now()
		review.save()
		# update clusters for the K Means algorithm
		update_clusters()
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button
		return HttpResponseRedirect(reverse('reviews:wine_detail', args=(wine.id,)))
	return render(
		request
		, 'reviews/wine_detail.html'
		, {'wine': wine, 'form': form}
	) #re-render with added view

# view for querying and adding a wine to the DB
@login_required
def add_wine(request):	
	form = WineForm(request.POST)
	if form.is_valid():
		#wine - form.save(commit=False)
		#name = form.cleaned_data['wine_name']
		#user_name = request.user.username
		wine = Wine()
		wine.name = form.cleaned_data['name']
		#wine.name = request.user.username
		wine.save()
		#return HttpResponseRedirect(reverse('reviews:wine_detail', args=(wine.id,)))
	wine_list = Wine.objects.order_by('-name')
	context = {'wine_list': wine_list}
	return render(request, 'reviews/wine_list.html', context)

# view for list of recommendations
@login_required
def recommendation_list(request):
	# getting reviews. prefetch many-to-many and many-to-one objects (many-to-one in this case)
	reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('wine')
	# generate a set of wine IDs from the result set
	reviews_wine_ids = set([r.wine.id for r in reviews])

	# retrieving which cluster the user belongs to
	try:
		cluster_name = \
			User.objects.get(username=request.user.username).cluster_set.first().name
	except: # if user does not belong to a cluster, update clusters to add this user to a cluster
		update_clusters()
		cluster_name = \
			User.objects.get(username=request.user.username).cluster_set.first().name

	# list of users in the cluster excluding self
	other_members = \
		Cluster.objects.get(name=cluster_name).users \
			.exclude(username=request.user.username).all()

	# generating as hashset from the list above
	other_members = set([u.username for u in other_members])
	
	# getting all reviews by other members of the cluster
	# exluce any wines that the current user has tried
	other_reviews = \
		Review.objects.filter(user_name__in=other_members) \
			.exclude(wine__id__in=reviews_wine_ids)

	# generate a set of wines from the result set above
	wines = set([r.wine.id for r in other_reviews])

	# generate a list of wines sorted descending by avg score 
	# referencing the Wine model for additional details
	wine_list = list(Wine.objects.filter(id__in=wines))
	wine_list.sort(key=lambda x: x.average_rating(), reverse=True)

	return render(
		request, 
		'reviews/recommendation_list.html'
		, {'username': request.user.username, 'wine_list': wine_list}
	)



