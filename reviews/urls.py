from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /
    url(r'^$', views.review_list, name='review_list'),
    # ex: /review/5/
    url(r'^review/(?P<review_id>[0-9]+)/$', views.review_detail, name='review_detail'),
    # ex: /wine/
    url(r'^wine$', views.wine_list, name='wine_list'),
    # ex: /wine/5/
    url(r'^wine/(?P<wine_id>[0-9]+)/$', views.wine_detail, name='wine_detail'),
	url(r'^wine/(?P<wine_id>[0-9]+)/add_review/$', views.add_review, name='add_review'),
	# when a user name is passed: show reviews for the logged user
	url(r'^review/user/(?P<username>\w+)/$', views.user_review_list, name='user_review_list'),
	# when a username is not passed: all reviews
	url(r'^review/user/$', views.user_review_list, name='user_review_list'),
    # page for adding wine
    url(r'^wine/add/$', views.wine_add, name='wine_add'),
    # additional api for adding wine
    url(r'^wine/add/add_wine/$', views.add_wine, name='add_wine'),
    # grabbing recommendations
    url(r'^recommendations/$', views.recommendation_list, name='recommendation_list'),
]