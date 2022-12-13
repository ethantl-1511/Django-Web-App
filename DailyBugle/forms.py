from django.forms import ModelForm
from .models import PeopleOfInterest, RandomFact

class PeopleOfInterestForm(ModelForm):
    class Meta:
        model = PeopleOfInterest
        fields = '__all__'

class RandomFactForm(ModelForm):
    class Meta:
        model = RandomFact
        fields = "__all__"