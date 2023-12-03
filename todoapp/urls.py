from . import views
from django.urls import path

urlpatterns = [
    path('home',views.home,name='home-page'),
    path('',views.register,name='register'),
    path('login',views.loginpage,name='login'),
     path('logout', views.LogoutView, name='logout'),
    path('delete-task/<str:name>', views.DeleteTask, name='delete'),
    path('update/<str:name>', views.Update, name='update'),
]
