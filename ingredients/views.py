import requests, os
from random import shuffle
from .models import Ingredient

from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DeleteView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

API_KEY = "80d739a457ba44e9a4e1ecfa120cd104"


class CustomLoginView(LoginView):
    template_name = 'ingredients/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('list-and-create')


class RegisterView(FormView):
    form_class = UserCreationForm
    template_name = "ingredients/register.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("list-and-create")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('list-and-create')
        return super(RegisterView, self).get(*args, **kwargs)


class ListAndCreate(LoginRequiredMixin, CreateView):
    model = Ingredient
    fields = ['name']
    template_name = "ingredients/ingredient_form.html"
    success_url = reverse_lazy('list-and-create')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredients"] = self.model.objects.all().filter(user=self.request.user)
        return context


class Ingredient_Delete(LoginRequiredMixin,DeleteView):
    model = Ingredient
    success_url = reverse_lazy('list-and-create')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

def RecipeView(request):
    if request.user.is_authenticated:
        if Ingredient.objects.all().filter(user=request.user):
            ingredients = Ingredient.objects.all().filter(user=request.user)
            list_of_ingredients = [i.name for i in ingredients]
            shuffle(list_of_ingredients)
            params = {
                "ingredients": list_of_ingredients,
                'number': 5,
                'limitLicense': False,
                'ranking': 1,
                'ignorePantry': True
            }
            response = requests.get(f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={API_KEY}", params=params).json()
            context = {
                "recipes": response
            }
            return render(request, 'ingredients/recipes.html', context)
        else:
            return HttpResponse("<h1>You have no ingredient</h1>")

    else:
        return redirect('login-user')


def RecipeDetail(request, id):
    if request.user.is_authenticated:
        response = requests.get(f"https://api.spoonacular.com/recipes/{id}/information?apiKey={API_KEY}").json()
        return redirect(response['spoonacularSourceUrl'])
    else:
        return redirect('login-user')
