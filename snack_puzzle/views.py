from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import View
import json
from django.contrib.auth import login, authenticate, logout
from django.views.generic import CreateView
from snack_puzzle.forms import LoginForm, AddUserForm
from snack_puzzle.serializers import RecipeSerializer
from .models import Category, Ingredient, Recipe, IngredientRecipe, User
from django.contrib.auth.mixins import LoginRequiredMixin

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

            for user_ingredients_dict in ingredients_data:
                ingredients.append(user_ingredients_dict['name'])

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
                    for user_ingredients_dict in ingredients_data:
                        if recipe_data.ingredient.name in user_ingredients_dict.values():
                            if recipe_data.measure == (user_ingredients_dict['measure']):
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
                recipe_true = remove_duplicates_in_list(recipe_true)
                for i in counter_dict:
                    if i.name in recipe_true and counter_dict[i] == len(i.ingredientrecipe_set.all()):
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


class RecipeCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Recipe
    fields = ['name', 'url', 'description', 'time']
    success_url = reverse_lazy("add_amount")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        self.object.user = user
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class IngredientRecipeCreateView(CreateView):
    model = IngredientRecipe
    fields = ['ingredient', 'amount', 'measure']
    success_url = reverse_lazy("add_amount")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        recipe = Recipe.objects.latest('id')
        self.object.recipe = recipe
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class LoginView(View):

    def get(self, request):
        return TemplateResponse(request, 'snack_puzzle/login.html', {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        ctx = {'form': form, 'message': None}
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                ctx.update({'message': 'Błąd loginu lub hasła'})
        return TemplateResponse(request, 'snack_puzzle/login.html', ctx)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('index')


class AddUserView(View):

    def get(self, request):
        form = AddUserForm()
        return TemplateResponse(request, 'snack_puzzle/user_form.html', {'form': form})

    def post(self, request):
        form = AddUserForm(request.POST)
        ctx = {'form': form}
        if form.is_valid():
            email = form.cleaned_data['login']
            password = form.cleaned_data['password']
            new_user = User.objects.create_user(username=email, email=email, password=password)
            login(request, new_user)
            return redirect('index')
        return TemplateResponse(request, 'snack_puzzle/user_form.html', ctx)