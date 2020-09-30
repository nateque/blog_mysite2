from django.urls import path
from blog import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/<slug>', views.detailPost, name='post_detail'),
]
