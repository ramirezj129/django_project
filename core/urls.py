from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name = "core-home"),
    path("about/", views.about, name = "core-about"),
    path("item/", views.item_list, name = "item"),
    path("<int:pk>/",views.detail, name="detail"),
    path("detail/",views.detail, name="detail"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("search/", views.search_bar, name = "search"),
    path('inbox/', views.inbox, name = 'inbox'),
    path('inbox/<int:pk>/', views.inbox_convo, name = 'inbox_convo')

    ]
