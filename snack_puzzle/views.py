from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views import View
import json
from snack_puzzle.serializers import RecipeSerializer
from .models import Category, Ingredient, Recipe

# Create your views here.


def remove_duplicates_in_list(l):
    return list(set(l))


def set_to_dump_list(dictionary, to_dump_list, recipe, ingredient):
    d = {'recipe_name': recipe, 'ingredient_name': ingredient}
    dictionary.update(d)
    to_dump_list.append(dictionary)
    return to_dump_list


class IndexView(View):

    def get(self, request):
        categories = Category.objects.order_by('name')
        ctx = {
            'slug': 'cat_',
            'categories': categories
        }
        return TemplateResponse(request, 'snack_puzzle/index.html', ctx)

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
            measure_dict = dict()
            measure_list = list()
            amount_dict = dict()
            amount_list = list()

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
                                    set_to_dump_list(amount_dict, amount_list, recipe.name, recipe_data.ingredient.name)
                                    break
                            else:
                                set_to_dump_list(measure_dict, measure_list, recipe.name, recipe_data.ingredient.name)
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

            to_dump['measure'] = measure_list
            to_dump['amount'] = amount_list
            print(serializer.data)

            return HttpResponse(json.dumps(to_dump))
        return TemplateResponse(request, 'snack_puzzle/index.html', ctx)


class IngredientDetailView(View):

    def get(self, request, pk):
        ingredient = Ingredient.objects.get(id=pk)
        recipes = ingredient.ingredientrecipe_set.all()
        ctx = {'ingredient': ingredient,
               'recipes': recipes}

        return TemplateResponse(request, 'snack_puzzle/ingredient_detail.html', ctx)



