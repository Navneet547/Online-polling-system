from django.urls import path
from accounts.views import *

app_name = "accounts"

urlpatterns = [
    path('login/',LoginView.as_view(),name="login"),
    path('register/',RegisterView.as_view(),name="register"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path('',Home.as_view(),name="home"),
    path('about/',About.as_view(),name="about"),
]
