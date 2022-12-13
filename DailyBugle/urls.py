from django.urls import path
from . import views

urlpatterns = [
    path('', views.dailyBugle_home, name="dailyBugle_home"),
    path('create/', views.dailyBugle_create, name="dailyBugle_create"),
    path('list/', views.dailyBugle_list, name="dailyBugle_list"),
    path('<int:pk>/details/', views.dailyBugle_details, name="dailyBugle_details"),
    path('<int:pk>/edit/', views.dailyBugle_edit, name="dailyBugle_edit"),
    path('<int:pk>/delete/', views.dailyBugle_delete, name="dailyBugle_delete"),
    path('api/', views.dailyBugle_api, name="dailyBugle_api"),
    path('bs/', views.dailyBugle_bs, name="dailyBugle_bs"),
    path('favorites/', views.dailyBugle_favoriteAPI, name="dailyBugle_favoriteAPI"),
    path('favorites/<int:id>', views.dailyBugle_deleteAPI, name="dailyBugle_deleteAPI"),
]