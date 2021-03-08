from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import UserSignUpView, UserSignInView, CoWorkersListView


urlpatterns = [
    path('register/', UserSignUpView.as_view(), name='register'),
    path('login/', UserSignInView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('coworkers/', CoWorkersListView.as_view(), name='coworkers')
]