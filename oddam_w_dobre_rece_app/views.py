from django.conf import settings
from django.contrib.auth import get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
# from django.core.serializers import json
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
# from django.utils import timezone
from django.views import View
from django.views.generic import FormView
import json

from oddam_w_dobre_rece_app.forms import RegisterForm, UserUpdateForm, PasswordChangeCustomForm
from oddam_w_dobre_rece_app.models import Donation, Institution, Category

User = get_user_model()


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
        organizations = Institution.objects.filter(type=2).order_by('pk')
        paginator2 = Paginator(organizations, 5)
        page2 = request.GET.get('page')
        org_page = paginator2.get_page(page2)

        # # Paginacja dla instytucji lokalnych
        locals = Institution.objects.filter(type=3).order_by('pk')
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


class GetInstitutionsByCategoryApi(View):
    def get(self, request):
        category_ids = request.GET.getlist('category_ids')
        institutions = Institution.objects.filter(categories__in=category_ids).distinct()
        institutions_data = []
        for institution in institutions:
            categories = institution.categories.all()
            category_names = [category.name for category in categories]
            institutions_data.append({
                'name': institution.name,
                'categories': category_names,
                'description': institution.description,
            })
        return JsonResponse(institutions_data, safe=False)


class AddDonation(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        context = {
            "categories": categories,
            "institutions": institutions,
        }
        return render(request, "oddam_w_dobre_rece_app/form.html", context)


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(request, 'oddam_w_dobre_rece_app/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse_lazy('landing-page'))
        else:
            # Check if email exists for alternative redirection
            email = request.POST.get('email')
            if email and get_user_model().objects.filter(email=email).exists():
                # If email exists but form is invalid, show errors
                return render(request, 'oddam_w_dobre_rece_app/login.html', {'form': form})
            else:
                # Redirect to register page if email does not exist
                return redirect(reverse_lazy('register'))

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class Register(View):
    def get(self, request, *args, **kwargs):
        form = RegisterForm
        return render(request, 'oddam_w_dobre_rece_app/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['email'],
                first_name=form.cleaned_data['name'],
                last_name=form.cleaned_data['surname'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
            )
            return redirect(reverse_lazy('login'))
        else:
            return render(request, 'oddam_w_dobre_rece_app/register.html', context)


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        donations = Donation.objects.filter(user=user).order_by('is_taken', '-pick_up_date')
        context = {
            'user': user,
            'donations': donations,
        }
        return render(request, 'oddam_w_dobre_rece_app/user_profile.html', context)

    def post(self, request, *args, **kwargs):
        user = request.user
        donation_id = request.POST.get('donation_id')
        donation = Donation.objects.get(id=donation_id, user=user)
        donation.is_taken = not donation.is_taken
        donation.save()
        return redirect('user-profile')


class SettingsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_form = UserUpdateForm(instance=request.user)
        password_form = PasswordChangeCustomForm(user=request.user)
        context = {
            'user_form': user_form,
            'password_form': password_form,
        }
        return render(request, 'oddam_w_dobre_rece_app/user_settings.html', context)

    def post(self, request, *args, **kwargs):
        if 'update_user' in request.POST:
            return self.handle_user_update(request)
        elif 'change_password' in request.POST:
            return self.handle_password_change(request)
        else:
            return self.get(request)

    def handle_user_update(self, request):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid() and request.user.check_password(user_form.cleaned_data['current_password']):
            user_form.save()
            return redirect('settings')

        return self.render_form(user_form=user_form)

    def handle_password_change(self, request):
        password_form = PasswordChangeCustomForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            return redirect('settings')
        return self.render_form(password_form=password_form)

    def render_form(self, user_form=None, password_form=None):
        context = {
            'user_form': user_form or UserUpdateForm(instance=self.request.user),
            'password_form': password_form or PasswordChangeCustomForm(user=self.request.user),
        }
        return render(self.request, 'oddam_w_dobre_rece_app/user_settings.html', context)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')


class SubmitDonation(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        quantity = data.get('bags')
        categories_ids = data.get('categories', [])
        institution_name = data.get('organization')
        address = data.get('address')
        city = data.get('city')
        zip_code = data.get('postcode')
        phone_number = data.get('phone')
        pick_up_date = data.get('data')
        pick_up_time = data.get('time')
        pick_up_comment = data.get('more_info', "Brak uwag")
        user = request.user

        try:
            institution = Institution.objects.get(name=institution_name)
        except Institution.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Nie ma takiej instytucji'}, status=400)

        categories = Category.objects.filter(id__in=categories_ids)

        donation = Donation.objects.create(
            quantity=quantity,
            institution=institution,
            address=address,
            phone_number=phone_number,
            city=city,
            zip_code=zip_code,
            pick_up_date=pick_up_date,
            pick_up_time=pick_up_time,
            pick_up_comment=pick_up_comment,
            user=user
        )
        donation.categories.set(categories)

        return JsonResponse({'success': True, 'redirect': 'form-confirmation'})


class FormConfirmationView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'oddam_w_dobre_rece_app/form-confirmation.html')
