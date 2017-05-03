from django.contrib import admin
from .models import Wine, Review, Cluster

# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
	model = Review
	# what columns do we wnat to display
	# in the order specified
	list_display = ('wine', 'rating', 'user_name', 'comment', 'pub_date')
	# list of filters
	list_filter = ['pub_date', 'user_name']
	# search box matching
	search_fields = ['comment']

class ClusterAdmin(admin.ModelAdmin):
	model = Cluster
	list_display = ['name', 'get_members']

admin.site.register(Wine)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Cluster, ClusterAdmin)