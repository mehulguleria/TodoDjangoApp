from django.urls import path

from app import views

urlpatterns = [
    path('',views.home,name="home"),
    path('register',views.registeruser,name='register'),
    path('verify/<str:email>',views.verify,name='verify'),
    path('login',views.userlogin,name='login'),
    path('logout',views.userlogout,name='logout'),
    path('profile',views.userprofile,name='profile'),
    path('createtodo',views.createtodo,name='createtodo'),
    path('profile/<int:id>',views.detailtodo,name='detailtodo'),
    path('completed/<int:id>',views.completetodo,name='completetodo'),
    path('history',views.history,name='history')
]