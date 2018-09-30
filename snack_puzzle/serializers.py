from rest_framework import serializers
from snack_puzzle.models import Category, Ingredient, Recipe, Meal, IngredientRecipe, Type


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'price', 'path']


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='get_name_display')
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'ingredients']


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'type', 'ingredient']


class IngredientRecipeSerializer(serializers.ModelSerializer):

    ingredient = IngredientSerializer(read_only=True)
    # recipe = RecipeSerializer(read_only=True)

    class Meta:
        model = IngredientRecipe
        fields = ['id', 'ingredient', 'amount']


class RecipeSerializer(serializers.ModelSerializer):
    # ingredient = IngredientSerializer(many=True, read_only=True)
    ingredient_recipe = IngredientRecipeSerializer(source='ingredientrecipe_set', many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'time', 'path', 'ingredient_recipe', 'user']


class MealSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='get_name_display')

    class Meta:
        model = Meal
        fields = ['id', 'name', 'recipe']



