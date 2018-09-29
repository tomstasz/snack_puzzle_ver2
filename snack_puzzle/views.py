from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
import json
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from snack_puzzle import serializers
from snack_puzzle.serializers import IngredientSerializer
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
        if 'sent_ingredients[]' in request.POST:
            ingredients = request.POST.getlist('sent_ingredients[]')
            ing_counted = Recipe.objects.annotate(cnt=Count('ingredient'))
            ing_reduced = ing_counted.filter(cnt=len(ingredients))
            # import ipdb;ipdb.set_trace()
            for ing in ingredients:
                ing_reduced = ing_reduced.filter(ingredient__name=ing)
            # to_ajax = json.dumps(ing_reduced)
            serializer = IngredientSerializer(instance=ing_reduced, many=True)
            # s = json.dumps(ingredients)
            # print(ingredients, s)
            return HttpResponse(json.dumps(serializer.data))
        return TemplateResponse(request, 'snack_puzzle/index.html', ctx)


class IngredientDetailView(View):

    def get(self, request, pk):
        ingredient = Ingredient.objects.get(id=pk)
        recipes = ingredient.ingredientrecipe_set.all()
        ctx = {'ingredient': ingredient,
               'recipes': recipes}

        return TemplateResponse(request, 'snack_puzzle/ingredient_detail.html', ctx)


class IngredientRecipeListView(ListCreateAPIView):
    serializer_class = serializers.IngredientRecipeSerializer
    queryset = IngredientRecipe.objects.all()


class IngredientRecipeDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.IngredientRecipeSerializer
    queryset = IngredientRecipe.objects.all()
