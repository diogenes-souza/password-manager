
from django.shortcuts import render, redirect
#from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Passwords #Meu modelo de dados
from .forms import PositionForm

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('passwords')


class registerPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = False
    success_url = reverse_lazy('passwords') #valor de re-direcionamento

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(registerPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('passwords')
        return super(registerPage, self).get(*args, **kwargs)

    

class passwordList(LoginRequiredMixin, ListView):
    model = Passwords
    context_object_name = 'passwords'

    def get_queryset(self):
        #passwords = Passwords.objects.filter(user=self.request.user)
        search_input = self.request.GET.get('search_') or ''
        if search_input:
            passwords = Passwords.objects.filter(siteTitle__icontains=search_input, user=self.request.user)
        else:
            passwords = Passwords.objects.all().filter(user=self.request.user)


        return passwords
        
    
class passwordDetail(LoginRequiredMixin, DetailView):
    model = Passwords
    context_object_name = 'password'
    template_name = 'base/password.html'



class passwordCreate(LoginRequiredMixin, CreateView):
    model = Passwords
    fields = ['siteTitle','websiteLink','websiteUser','websiteEmail','websitePassword']
    success_url = reverse_lazy('passwords') #valor de re-direcionamento
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(passwordCreate, self).form_valid(form)


class passwordUpdate(LoginRequiredMixin, UpdateView):
    model = Passwords
    fields = ['siteTitle','websiteLink','websiteUser','websiteEmail','websitePassword']
    success_url = reverse_lazy('passwords') #valor de re-direcionamento

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Passwords
    context_object_name = 'password'
    success_url = reverse_lazy('passwords') #valor de re-direcionamento


class passwordReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_password_order(positionList)

        return redirect(reverse_lazy('passwords'))