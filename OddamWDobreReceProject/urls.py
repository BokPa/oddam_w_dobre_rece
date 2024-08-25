"""
URL configuration for DndOrganizerProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

#from dnd_organizer_app import views as dnd_views
from oddam_w_dobre_rece_app import views as oddam_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', oddam_views.LandingPage.as_view(), name="landing-page"),
    path('add-donation/', oddam_views.AddDonation.as_view(), name="add-donation"),
    path('institution-by-category/', oddam_views.GetInstitutionsByCategoryApi.as_view(), name="institution-by-category"),
    path('login/', oddam_views.LoginView.as_view(), name="login"),
    path('register/', oddam_views.Register.as_view(), name="register"),
    path('profile/', oddam_views.ProfileView.as_view(), name="profile"),
    path('settings/', oddam_views.SettingsView.as_view(), name="settings"),
    path('logout/', oddam_views.LogoutView.as_view(), name="logout"),
    path('add-donation/form-confirmation/', oddam_views.FormConfirmationView.as_view(), name='form-confirmation'),

]
