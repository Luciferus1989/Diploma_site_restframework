from django.urls import path
from .views import (login_view,
                    logout_view, RegisterView,)

app_name = 'myauth'

urlpatterns = [
    path('sign-in/', login_view, name='sign-in'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]

