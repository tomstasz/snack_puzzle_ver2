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


def remove_duplicates_in_list(l):
    return list(set(l))


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
    #         for recipe in res:
    #             print(recipe.time)
    #             for recipe_data in recipe.ingredientrecipe_set.all():
    #                 print(recipe_data.ingredient.name, recipe_data.measure)
    #
    #         print(serializer.data)
    #
    #         return HttpResponse(json.dumps(serializer.data))
    #     return TemplateResponse(request, 'snack_puzzle/index.html', ctx)

    def post(self, request):
        ctx = {'ing_sent': "empty"}
        if 'data' in request.POST:
            data = json.loads(request.POST['data'])
            ingredients_data = data['ingredients']
            ingredients = []
            print('-------')
            for user_ingredients_dict in ingredients_data:
                ingredients.append(user_ingredients_dict['name'])

                print(user_ingredients_dict['name'], user_ingredients_dict['amount'], user_ingredients_dict['measure'])
            print('-------')

            res = Recipe.objects.filter(
                ingredient__name__in=ingredients).exclude(
                ingredient__in=Ingredient.objects.exclude(
                    name__in=ingredients)).distinct('id')
            serializer = RecipeSerializer(instance=res, many=True)

            to_dump = {'serial': serializer.data}

            cooking_flag = False
            recipe_true = []
            counter_dict = dict()
            ready_to_cook = []

            for recipe in res:
                counter_dict[recipe] = 0
                for recipe_data in recipe.ingredientrecipe_set.all():
                    print("(recipe_data) Ingredient name: " + recipe_data.ingredient.name)
                    for user_ingredients_dict in ingredients_data:
                        if recipe_data.ingredient.name in user_ingredients_dict.values():
                            print("Sprawdzam: " + recipe_data.measure, user_ingredients_dict['measure'])
                            if recipe_data.measure == (user_ingredients_dict['measure']):
                                print(float(user_ingredients_dict['amount']), float(recipe_data.amount))
                                if (float(user_ingredients_dict['amount'])) >= (float(recipe_data.amount)):
                                    cooking_flag = True
                                    recipe_true.append(recipe.name)
                                    counter_dict[recipe] += 1

                                else:
                                    print("Wrong amount")
                                    print(recipe.name, recipe_data.ingredient.name)
                                    break
                            else:
                                print("Wrong measure")
                                print(recipe.name, recipe_data.ingredient.name)
                                break

            if cooking_flag:
                print("Counter: ", counter_dict)
                print('Recipe_true:', recipe_true)
                recipe_true = remove_duplicates_in_list(recipe_true)
                print('Recipe_true_set:', recipe_true)
                for i in counter_dict:
                    if i.name in recipe_true and counter_dict[i] == len(i.ingredientrecipe_set.all()):
                        print("Sukces, możesz przygotować ", i.name)
                        ready_to_cook.append(i.name)
                        ready_to_cook = remove_duplicates_in_list(ready_to_cook)
                        to_dump['ready'] = ready_to_cook

            print(serializer.data)

            # return HttpResponse(json.dumps(serializer.data))
            return HttpResponse(json.dumps(to_dump))
        return TemplateResponse(request, 'snack_puzzle/index.html', ctx)


class IngredientDetailView(View):

    def get(self, request, pk):
        ingredient = Ingredient.objects.get(id=pk)
        recipes = ingredient.ingredientrecipe_set.all()
        ctx = {'ingredient': ingredient,
               'recipes': recipes}

        return TemplateResponse(request, 'snack_puzzle/ingredient_detail.html', ctx)



