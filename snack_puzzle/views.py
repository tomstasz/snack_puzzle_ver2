from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from .models import Category, Ingredient, Recipe, Meal, IngredientRecipe
# Create your views here.


class IndexView(View):

    def get(self, request):
        all_categories = Category.objects.order_by('name')
        ingredients = Ingredient.objects.filter(category=1)
        ctx = {
            'categories': all_categories,
            'slug': 'cat_',
            'ingredients': ingredients
        }
        recipe = Recipe.objects.get(id=1)

        ctx.update({
            'recipe': recipe
        })
        return TemplateResponse(request, 'snack_puzzle/index.html', ctx)

    def post(self, request):
        ctx = {'ing_sent': "empty"}
        if 'sent_ingredients' in request.POST:
            ingredients = request.POST.get('sent_ingredients')
            ctx = {'ing_sent': ingredients}
            return TemplateResponse(request, 'snack_puzzle/index.html', ctx)
        return TemplateResponse(request, 'snack_puzzle/index.html', ctx)


class IngredientDetailView(View):

    def get(self, request, pk):
        ingredient = Ingredient.objects.get(id=pk)
        recipes = ingredient.ingredientrecipe_set.all()
        ctx = {'ingredient': ingredient,
               'recipes': recipes}

        return TemplateResponse(request, 'snack_puzzle/ingredient_detail.html', ctx)


class IngredientCheck(View):
    def post(self, request):
        ctx = {'ing_sent': "empty"}
        if 'sent_ingredients' in request.POST:
            ingredients = request.POST.get('sent_ingredients')
            ctx = {'ing_sent': ingredients}
            return TemplateResponse(request, 'snack_puzzle/try_ajax.html', ctx)
        return TemplateResponse(request, 'snack_puzzle/try_ajax.html', ctx)
