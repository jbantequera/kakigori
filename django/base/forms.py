from django.forms import ModelForm, HiddenInput
from .models import Profile, Recipe

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name', 'bio']
        
class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'instructions']