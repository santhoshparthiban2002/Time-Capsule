from django.urls import path,include
from .views import *
urlpatterns = [
    path("",register,name="register"),
    path("login/",login,name="login"),
    path("logout/",logout,name="logout"),
    path("manager/",manager_index,name="index"),
    path("manager/profile",manager_profile,name="profile"),
    path("manager/profile/<str:username>",user_profile,name="user_profile"),
    path("manager/profile/update_password/<str:username>",update_password,name="update_password"),
    path("manager/users",manager_users,name="users"),
    path("manager/delivery",manager_delivery,name="delivery"),
    path("manager/delivered",manager_delivered,name="delivered"),
    path("timecapsule/<str:username>",timecapsule,name="timecapsule"),

]