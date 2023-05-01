from django.shortcuts import render
from django.views.generic import *
from .models import *


class HomeView(TemplateView):
    template_name = 'home.html'

