from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('company/<str:pk>/', views.company_detail, name="company-detail"),
    path('account/', views.account, name='account'),
    path('plan/change', views.change_plan, name='change-plan'),
    path('plan/delete', views.plan_cancelation, name='cancel-plan'),

    path('login', views.loginuser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.registerUser, name='register'),

]
