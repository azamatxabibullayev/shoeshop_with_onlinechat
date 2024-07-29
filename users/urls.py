from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('welcome/', views.welcome, name='welcome'),
    path('logout/', views.logout_view, name='logout'),
    path('upload/', views.upload_painting, name='upload_painting'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('inbox/', views.inbox, name='inbox'),
    path('send_message/<str:recipient_username>/', views.send_message, name='send_message'),
    path('notifications/', views.notifications, name='notifications'),
]