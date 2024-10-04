from django.urls import path

from user.views import CustomLoginView, RegisterView, LogoutView

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]