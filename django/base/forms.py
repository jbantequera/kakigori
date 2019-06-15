from django.forms import ModelForm, HiddenInput, CharField
from .models import Profile, Recipe

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name', 'bio', 'image']

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'instructions', 'image', 'cooking_time']