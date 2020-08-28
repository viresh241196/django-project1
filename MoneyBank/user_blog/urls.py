from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='user_home'),
    path('new_post', views.new_post, name='new_post'),
    path('detail_post/<int:id>/', views.detail_post, name='detail_post'),
    path('user_posts/<int:author_id>/', views.user_post, name='user_posts'),
]