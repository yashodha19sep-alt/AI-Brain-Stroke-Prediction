from django.urls import path
from .import views
urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('login/', views.login, name='login'),
    path('main/', views.main, name='main'),
    path('',views.home, name='home'),
]

