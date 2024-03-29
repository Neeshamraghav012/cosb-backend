from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [

    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('', views.getRoutes),
    path('test/', views.testEndPoint, name='test'),
    path('course-status/', views.StatusView, name = 'course-status'),
    path('cosb-id/', views.cosbid, name = 'cosb-id'),
    path('profile-view/', views.profileView, name = 'profile-view'),
    path('profile-view/<str:username>/', views.profileViewByName, name = 'profile-view-by-name'),



]

# https://cosbapi.herokuapp.com/api/user/token/ for login
# https://cosbapi.herokuapp.com/api/user/token/refresh/ for refresh token
# https://cosbapi.herokuapp.com/api/user/register/      for sign up
