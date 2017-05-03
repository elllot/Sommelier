from django.forms import ModelForm, Textarea, TextInput
from reviews.models import Review, Wine

class ReviewForm(ModelForm):
	class Meta:
		model = Review
		fields = ['rating', 'comment']
		widgets = {
			'comment': Textarea(attrs={'cols': 40, 'rows': 15})
		}

class WineForm(ModelForm):
	class Meta:
		model = Wine
		fields = ['name']
		widgets = {
			'name' : TextInput(attrs = {'placeholder': 'Wine Name'}),
			#'name': Textarea(attrs={'cols': 40, 'rows': 15})
		}
