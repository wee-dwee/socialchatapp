from django.urls import path
from .views import *

urlpatterns=[
    path('home',home,name='home'),
    path('signup/',signup,name='signup'),
    path('signin/',signin,name='signin'),
    path('logout/',logout,name='logout'),
    path('follow',follow,name='follow'),
    path('search',search,name='search'),
    path('settings/',settings,name='settings'),
    path('upload',upload,name='upload'),
    path('like_post',likepost,name='like_post'),
    path('profile/<str:pk>',profile,name='profile'),
    
]