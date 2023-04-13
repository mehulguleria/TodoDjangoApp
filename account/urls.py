from django.urls import path
# from rest_framework.authtoken.views import obtain_auth_token

from account.views import RegistrationAPIView,LogoutAPIView,VerifyUser,LoginAPIView

urlpatterns = [
    path('api/login',LoginAPIView.as_view(),name="api-login"),
    path('api/register',RegistrationAPIView.as_view(),name="api-register"),
    path('api/logout',LogoutAPIView.as_view(),name="api-logout"),
    
    path('api/<str:email>/verify/<int:code>',VerifyUser.as_view(),name="api-verify")
]