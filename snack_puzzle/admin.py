from django.contrib import admin
from .models import Category, Ingredient, Type, Recipe, Meal, IngredientRecipe


# Register your models here.


admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Type)
admin.site.register(Recipe)
admin.site.register(Meal)
admin.site.register(IngredientRecipe)