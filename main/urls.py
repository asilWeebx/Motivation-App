from django.urls import path
from .views import my_functional_view, Logout, index, search, status, LOGINN, doLogin, dashboard_admin

urlpatterns = [
    path("signup/",my_functional_view,name="signup"),
    path('logout/',Logout,name="logout"),
    path('accounts/profile/',index,name="index"),
    path('',index,name="index"),
    path('search/', search, name='search'),
    path('status/<int:id>/',status,name='status'),
    path('login/', LOGINN, name='loginn'),
    path('doLogin/', doLogin, name='doLogin'),
    path('dashboard_admin/',dashboard_admin,name="dashboard_admin"),

]