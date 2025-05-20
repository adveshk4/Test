from django.test import TestCase
from .models import Ingredient, Recipe

class CoreModelsTest(TestCase):
    def test_ingredient_creation(self):
        ing = Ingredient.objects.create(name='Kale')
        self.assertEqual(str(ing), 'Kale')

    def test_recipe_and_ingredients(self):
        i1 = Ingredient.objects.create(name='Tomato')
        i2 = Ingredient.objects.create(name='Basil')
        r = Recipe.objects.create(title='Tomato Soup', description='Cozy soup')
        r.ingredients.add(i1, i2)
        self.assertEqual(r.ingredients.count(), 2)
