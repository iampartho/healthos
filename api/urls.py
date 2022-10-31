from django.urls import path
from . import views


urlpatterns = [

    path('', views.getRoutes),
    path('company/', views.getCompany),
    path('company/<str:pk>/', views.getCompanyUsers),
    path('company/<str:pk>/noplan', views.getCompanyUsersWithNoPlan),
    path('company/<str:pk>/paiduser', views.getCompanyPaidUsers),
    path('company/<str:pk>/nonpaiduser', views.getCompanyNonPaidUsers),
    path('company/<str:pk1>/user/<str:pk2>/charge', views.chargeCompanyUser),
    path('company/<str:pk1>/user/<str:pk2>/cancel', views.cancelDataPlan),
    # path('projects/<str:pk>/vote/', views.projectVote),
    #
    # path('remove-tag/', views.removeTag)
]
