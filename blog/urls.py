from django.urls import path
from blog import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/<slug>', views.detailPost, name='post_detail'),
    path('post/new', views.createPost, name='create'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_registration, name='register'),
    path('profile/', views.profileEdit, name='profile'),
]
