from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.ProfileView.as_view()),
    path('register/', views.RegisterApiView.as_view()),
    path('login/', views.LoginApiView.as_view()),
    path('activate/<uuid:activation_code>/', views.ActivationView.as_view(), name='activation_code'),
]