from django.urls import path
from .views import my_functional_view, Logout, index, search, status, LOGINN, doLogin, dashboard_admin, favourite, \
    sevimli, category_filter, statusadd, users_status, users_status_get, my_status, edit, delete

urlpatterns = [
    path("signup/",my_functional_view,name="signup"),
    path('logout/',Logout,name="logodut"),
    path('accounts/profile/',index,name="index"),
    path('',index,name="index"),
    path('search/', search, name='search'),
    path('status/<int:id>/',status,name='status'),
    path('login/', LOGINN, name='loginn'),
    path('doLogin/', doLogin, name='doLogin'),
    path('dashboard_admin/',dashboard_admin,name="dashboard_admin"),
    path('favourite/<int:id>/', favourite, name='favourites'),
    path('favourites/', sevimli, name='sevimli'),
    path('category/<int:id>/',category_filter,name="category_filter"),
    path('status_add/',statusadd,name="status_add"),
    path('users_status/',users_status,name='users_status'),
    path('users_status/<int:id>/',users_status_get,name='users_status_get'),
    path('my_status/',my_status,name="my_status"),
    path('edit/<int:id>/',edit,name="edit"),
    path('delete/<int:id>/',delete,name="delete")
]