from django.conf import settings
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import FormView

from oddam_w_dobre_rece_app.models import Donation, Institution, Category


class LandingPage(View):
    def get(self, request, *args, **kwargs):
        bags_total = Donation.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
        supported_institutions = Institution.objects.filter(donation__isnull=False).distinct().count()

        # Paginacja dla fundacji
        foundations = Institution.objects.filter(type=1).order_by('pk')
        paginator1 = Paginator(foundations, 5)
        page1 = request.GET.get('page')
        found_page = paginator1.get_page(page1)

        # # Paginacja dla organizacji
        organizations = Institution.objects.filter(type=2)
        paginator2 = Paginator(organizations, 5)
        page2 = request.GET.get('page')
        org_page = paginator2.get_page(page2)

        # # Paginacja dla instytucji lokalnych
        locals = Institution.objects.filter(type=3)
        paginator3 = Paginator(locals, 5)
        page3 = request.GET.get('page')
        loc_page = paginator3.get_page(page3)


        context = {
            'bags_total': bags_total,
            'supported_institutions': supported_institutions,
            'found_page': found_page,
            'org_page': org_page,
            'loc_page': loc_page,
        }
        return render(request, "oddam_w_dobre_rece_app/index.html", context)

class AddDonation(View):
    def get(self, request, *args, **kwargs):
        return render(request, "oddam_w_dobre_rece_app/form.html")

class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request, "oddam_w_dobre_rece_app/login.html")

class Register(View):
    def get(self, request, *args, **kwargs):
        return render(request, "oddam_w_dobre_rece_app/register.html")