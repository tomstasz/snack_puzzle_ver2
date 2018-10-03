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
from snack_puzzle.serializers import IngredientSerializer, RecipeSerializer
from .models import Category, Ingredient, Recipe, Meal, IngredientRecipe
# Create your views here.


class IndexView(View):

    def get(self, request):
        categories = Category.objects.order_by('name')
        example_ingredients = Ingredient.objects.filter(category=1)

        ctx = {
            'slug': 'cat_',
            'example_ingredients': example_ingredients
        }
        recipe = Recipe.objects.get(id=1)
        ingredients = recipe.ingredientrecipe_set.all()

        ctx.update({
            'categories': categories,
            'recipe': recipe,
            'ingredients': ingredients
        })

        return TemplateResponse(request, 'snack_puzzle/index.html', ctx)

    # def post(self, request):
    #     ctx = {'ing_sent': "empty"}
    #     if 'sent_ingredients[]' in request.POST:
    #         ingredients = request.POST.getlist('sent_ingredients[]')
    #         res = Recipe.objects.filter(
    #             ingredient__name__in=ingredients).exclude(
    #             ingredient__in=Ingredient.objects.exclude(
    #                 name__in=ingredients)).distinct('id')
    #         serializer = RecipeSerializer(instance=res, many=True)
    #
    #         print(serializer.data)
    #
    #         return HttpResponse(json.dumps(serializer.data))
    #     return TemplateResponse(request, 'snack_puzzle/index.html', ctx)

    def post(self, request):
        ctx = {'ing_sent': "empty"}
        if 'sent_ingredients[]' in request.POST:
            ingredients_received = request.POST.getlist('sent_ingredients[]')
            ingredients_received = json.loads(ingredients_received)
            ingredients = []
            for dictionary in ingredients_received:
                ingredients.append(dictionary['name'])
            print(ingredients)

            res = Recipe.objects.filter(
                ingredient__name__in=ingredients).exclude(
                ingredient__in=Ingredient.objects.exclude(
                    name__in=ingredients)).distinct('id')
            serializer = RecipeSerializer(instance=res, many=True)

            print(serializer.data)

            return HttpResponse(json.dumps(serializer.data))
        return TemplateResponse(request, 'snack_puzzle/index.html', ctx)


class IngredientDetailView(View):

    def get(self, request, pk):
        ingredient = Ingredient.objects.get(id=pk)
        recipes = ingredient.ingredientrecipe_set.all()
        ctx = {'ingredient': ingredient,
               'recipes': recipes}

        return TemplateResponse(request, 'snack_puzzle/ingredient_detail.html', ctx)



