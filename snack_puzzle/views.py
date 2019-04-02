import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from snack_puzzle.forms import LoginForm, AddUserForm, TimeSearchForm
from snack_puzzle.serializers import RecipeSerializer
from .models import Category, Ingredient, Recipe, IngredientRecipe, User


# Create your views here.


def remove_duplicates_in_list(recipe_list):
    """Remove duplicates in recipe list"""
    return list(set(recipe_list))


def set_to_dump_list(dictionary, to_dump_list, recipe, ingredient):
    """Prepare list of recipes"""
    d = {'recipe_name': recipe, 'ingredient_name': ingredient}
    dictionary.update(d)
    to_dump_list.append(dictionary)
    return to_dump_list


class IndexView(View):
    """Main page with all the categories and user-generated recipes"""

    def get(self, request):
        """Show all ingredient categories"""
        categories = Category.objects.order_by('name')
        ctx = {
            'slug': 'cat_',
            'categories': categories
        }
        return TemplateResponse(request, 'snack_puzzle/index.html', ctx)

    def post(self, request):
        """Check if you can generate any recipe based on user ingredients"""
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
                        if (recipe_data.ingredient.name
                                in user_ingredients_dict.values()):
                            if (recipe_data.measure
                                    == (user_ingredients_dict['measure'])):
                                if ((float(user_ingredients_dict['amount']))
                                        >= (float(recipe_data.amount))):
                                    cooking_flag = True
                                    recipe_true.append(recipe.name)
                                    counter_dict[recipe] += 1

                                else:
                                    set_to_dump_list(
                                        amount_dict,
                                        amount_list,
                                        recipe.name,
                                        recipe_data.ingredient.name
                                    )
                                    break
                            else:
                                set_to_dump_list(measure_dict,
                                                 measure_list,
                                                 recipe.name,
                                                 recipe_data.ingredient.name)
                                break

            if cooking_flag:
                recipe_true = remove_duplicates_in_list(recipe_true)
                for i in counter_dict:
                    if (i.name in recipe_true
                            and counter_dict[i]
                            == len(i.ingredientrecipe_set.all())):
                        ready_to_cook.append(i.name)
                        ready_to_cook = remove_duplicates_in_list(
                            ready_to_cook
                        )
                        to_dump['ready'] = ready_to_cook

            to_dump['measure'] = measure_list
            to_dump['amount'] = amount_list
            print(serializer.data)

            return HttpResponse(json.dumps(to_dump))
        return TemplateResponse(request, 'snack_puzzle/index.html', ctx)


class IngredientDetailView(View):
    """More information about selected ingredient"""

    def get(self, request, pk):
        """Show all available recipes with selected ingredient"""
        ingredient = Ingredient.objects.get(id=pk)
        recipes = ingredient.ingredientrecipe_set.all()
        ctx = {'ingredient': ingredient,
               'recipes': recipes}

        return TemplateResponse(request,
                                'snack_puzzle/ingredient_detail.html',
                                ctx)


class RecipeCreateView(LoginRequiredMixin, CreateView):
    """Allow authenticated users to create their own recipe"""
    login_url = 'login'
    model = Recipe
    fields = ['name', 'url', 'description', 'time']
    success_url = reverse_lazy("add_amount")

    def form_valid(self, form):
        """If all fields are valid, send recipe to database"""
        self.object = form.save(commit=False)
        user = self.request.user
        self.object.user = user
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class IngredientRecipeCreateView(CreateView):
    """Specify amount and measure of each ingredient in user created recipe"""
    model = IngredientRecipe
    fields = ['ingredient', 'amount', 'measure']
    success_url = reverse_lazy("add_amount")

    def form_valid(self, form):
        """If all fields are valid, send ingredients details to database"""
        self.object = form.save(commit=False)
        recipe = Recipe.objects.latest('id')
        self.object.recipe = recipe
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class LoginView(View):
    """Authenticate users"""

    def get(self, request):
        """Show login form"""
        return TemplateResponse(request,
                                'snack_puzzle/login.html',
                                {'form': LoginForm()})

    def post(self, request):
        """Allow authenticated user to log in"""
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
    """Log out current user"""

    def get(self, request):
        """Log out and show main page"""
        logout(request)
        return redirect('index')


class AddUserView(View):
    """Create new user account"""

    def get(self, request):
        """Show form with user data"""
        form = AddUserForm()
        return TemplateResponse(request,
                                'snack_puzzle/user_form.html',
                                {'form': form})

    def post(self, request):
        """If all fields are valid, add new user to database"""
        form = AddUserForm(request.POST)
        ctx = {'form': form}
        if form.is_valid():
            email = form.cleaned_data['login']
            password = form.cleaned_data['password']
            new_user = User.objects.create_user(username=email,
                                                email=email,
                                                password=password)
            login(request, new_user)
            return redirect('index')
        return TemplateResponse(request, 'snack_puzzle/user_form.html', ctx)


class TimeSearch(View):
    """Search recipes based on time necessary to prepare them"""
    def get(self, request):
        """Allow user to specify time"""
        form = TimeSearchForm()
        return TemplateResponse(request,
                                'snack_puzzle/time_search_form.html',
                                {'form': form})

    def post(self, request):
        """Show all recipes matching specified time"""
        form = TimeSearchForm(request.POST)
        ctx = {'form': form}
        if form.is_valid():
            time = form.cleaned_data['time']
            recipes = Recipe.objects.filter(time__lte=int(time))
            ctx.update({'recipes': recipes})
        return TemplateResponse(request,
                                'snack_puzzle/time_search_form.html',
                                ctx)
