from django.conf import settings
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import FormView

class LandingPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, "oddam_w_dobre_rece_app/index.html")

class AddDonation(View):
    def get(self, request, *args, **kwargs):
        return render(request, "oddam_w_dobre_rece_app/form.html")

class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request, "oddam_w_dobre_rece_app/login.html")

class Register(View):
    def get(self, request, *args, **kwargs):
        return render(request, "oddam_w_dobre_rece_app/register.html")