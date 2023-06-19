from django.urls import path
from .views import *
urlpatterns = [
    path('',home,name='home'),
    path('data/',data,name='data'),
    path('signin/',login_user,name='login'),
    path('logout/',logout_user,name='logout'),
    path('signup/',register_user,name='signup'),
    path('auth/',isAuth,name='isAuth'),
    path('blogs/<str:blogname>/', blogdetail, name='blogdetail'),
    path('addblog/',addBlog,name='addblog'),
    path('updateblog/<str:blogname>/',updateBlog,name='updateblog'),
    path('deleteblog/<str:blogslug>/',deleteBlog,name='deleteblog'),
    path('account/',account,name='account'),
]