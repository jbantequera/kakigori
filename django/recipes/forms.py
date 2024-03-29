from django.forms import ModelForm
from .models import Recipe

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'ingredients', 'instructions', 'image', 'cooking_time']