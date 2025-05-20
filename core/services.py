from .models import Ingredient, Recipe
from .serializers import IngredientSerializer, RecipeSerializer
from graphql import GraphQLError

def create_ingredient_service(data):
    serializer = IngredientSerializer(data=data)
    if serializer.is_valid():
        return serializer.save()
    raise GraphQLError(f"Failed to create ingredient: {serializer.errors}")

def update_ingredient_service(pk, data):
    try:
        instance = Ingredient.objects.get(pk=pk)
    except Ingredient.DoesNotExist:
        raise GraphQLError("Ingredient not found.")
    serializer = IngredientSerializer(instance, data=data, partial=True)
    if serializer.is_valid():
        return serializer.save()
    raise GraphQLError(f"Failed to update ingredient: {serializer.errors}")

def delete_ingredient_service(pk):
    try:
        ing = Ingredient.objects.get(pk=pk)
    except Ingredient.DoesNotExist:
        raise GraphQLError("Ingredient not found.")
    ing.delete()
    return True

def create_recipe_service(data):
    serializer = RecipeSerializer(data=data)
    if serializer.is_valid():
        return serializer.save()
    raise GraphQLError(f"Failed to create recipe: {serializer.errors}")

def add_ingredients_service(recipe_id, ingredient_ids):
    try:
        recipe = Recipe.objects.get(pk=recipe_id)
    except Recipe.DoesNotExist:
        raise GraphQLError("Recipe not found.")
    ingredients = Ingredient.objects.filter(pk__in=ingredient_ids)
    if not ingredients.exists():
        raise GraphQLError("No valid ingredients to add.")
    recipe.ingredients.add(*ingredients)
    return recipe

def remove_ingredients_service(recipe_id, ingredient_ids):
    try:
        recipe = Recipe.objects.get(pk=recipe_id)
    except Recipe.DoesNotExist:
        raise GraphQLError("Recipe not found.")
    ingredients = Ingredient.objects.filter(pk__in=ingredient_ids)
    recipe.ingredients.remove(*ingredients)
    return recipe
