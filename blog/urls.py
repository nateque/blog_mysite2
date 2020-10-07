from django.urls import path
from blog import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/<slug>', views.detailPost, name='post_detail'),
    path('post/new', views.createPost, name='create'),
    path('post/edit/<int:id>', views.edit_post, name='edit_post'),
    path('post/delete/<int:id>', views.delete_post, name='delete_post'),
    path('comment/delete/<int:id>', views.delete_comment, name='delete_comment'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_registration, name='register'),
    path('profile/', views.profileEdit, name='profile'),
    path('like/', views.like_post, name='like_post'),
]
