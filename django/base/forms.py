from django.forms import ModelForm, HiddenInput, CharField, Textarea
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, Recipe

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name', 'bio', 'image']

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'instructions', 'image', 'cooking_time']

class SignupForm(UserCreationForm):
    display_name = CharField(max_length=15)
    bio = CharField(widget=Textarea, max_length=256, required=False)

    class Meta:
        model = User
        fields = ['username', 'display_name', 'bio', 'password1']