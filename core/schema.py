import strawberry
from typing import List, Optional
from strawberry.types import Info
from .models import Ingredient, Recipe
from .services import (
    create_ingredient_service,
    update_ingredient_service,
    delete_ingredient_service,
    create_recipe_service,
    add_ingredients_service,
    remove_ingredients_service,
)
from graphql import GraphQLError

@strawberry.type
class IngredientType:
    id: strawberry.ID
    name: str

@strawberry.type
class RecipeType:
    id: strawberry.ID
    title: str
    description: Optional[str]
    ingredients: List[IngredientType]
    ingredient_count: int

def to_ingredient_type(ing: Ingredient) -> IngredientType:
    return IngredientType(id=strawberry.ID(str(ing.id)), name=ing.name)

def to_recipe_type(recipe: Recipe) -> RecipeType:
    ings = list(recipe.ingredients.all())
    return RecipeType(
        id=strawberry.ID(str(recipe.id)),
        title=recipe.title,
        description=recipe.description,
        ingredients=[to_ingredient_type(i) for i in ings],
        ingredient_count=len(ings),
    )

@strawberry.type
class IngredientListType:
    items: List[IngredientType]
    total_count: int
    page: int
    page_size: int

@strawberry.type
class Query:
    @strawberry.field
    def list_ingredients(
        self,
        info: Info,
        filter: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> IngredientListType:
        qs = Ingredient.objects.order_by('name')
        if filter:
            qs = qs.filter(name__icontains=filter)
        total = qs.count()
        start = (page - 1) * page_size
        items = qs[start : start + page_size]
        return IngredientListType(
            items=[to_ingredient_type(i) for i in items],
            total_count=total,
            page=page,
            page_size=page_size,
        )

    @strawberry.field
    def get_recipe(self, info: Info, id: strawberry.ID) -> RecipeType:
        try:
            recipe = Recipe.objects.get(pk=id)
        except Recipe.DoesNotExist:
            raise GraphQLError("Recipe not found.")
        return to_recipe_type(recipe)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_ingredient(self, info: Info, name: str) -> IngredientType:
        ing = create_ingredient_service({'name': name})
        return to_ingredient_type(ing)

    @strawberry.mutation
    def update_ingredient(self, info: Info, id: strawberry.ID, name: str) -> IngredientType:
        ing = update_ingredient_service(id, {'name': name})
        return to_ingredient_type(ing)

    @strawberry.mutation
    def delete_ingredient(self, info: Info, id: strawberry.ID) -> bool:
        return delete_ingredient_service(id)

    @strawberry.mutation
    def create_recipe(
        self,
        info: Info,
        title: str,
        description: Optional[str] = None,
        ingredient_ids: Optional[List[strawberry.ID]] = None,
    ) -> RecipeType:
        data = {
            'title': title,
            'description': description or '',
            'ingredient_ids': ingredient_ids or [],
        }
        recipe = create_recipe_service(data)
        return to_recipe_type(recipe)

    @strawberry.mutation
    def add_ingredients_to_recipe(
        self,
        info: Info,
        recipe_id: strawberry.ID,
        ingredient_ids: List[strawberry.ID],
    ) -> RecipeType:
        recipe = add_ingredients_service(recipe_id, ingredient_ids)
        return to_recipe_type(recipe)

    @strawberry.mutation
    def remove_ingredients_from_recipe(
        self,
        info: Info,
        recipe_id: strawberry.ID,
        ingredient_ids: List[strawberry.ID],
    ) -> RecipeType:
        recipe = remove_ingredients_service(recipe_id, ingredient_ids)
        return to_recipe_type(recipe)
