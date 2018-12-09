from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.Register.as_view(), name='register_company'),
    path('login/', views.Login.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='view_profile'),
    path('company/', views.CompanyView.as_view(), name='view_company'),
    path('employee/', views.EmployeeView.as_view(), name='view_employee'),
    path('logout/', views.Logout.as_view(), name='logout')
]