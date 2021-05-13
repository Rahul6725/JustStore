from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name="welcome"),
    path('upload/', views.upload, name="upload"),
    path('uploadingsongs/', views.uploadingsongs, name="uploadingsongs"),
    path('uploaded/', views.uploaded, name="uploaded"),
    # path('signup', views.signup, name="signup"),
    # path('login', views.login, name="login"),
    # path('logout', views.logout, name="logout"),
    # path('home', views.home, name="home"),
    # path('account', views.account, name="account"),
    # path('detectface', views.detectface, name="detectface"),
]
