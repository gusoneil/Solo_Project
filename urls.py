from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('main', views.main),
    path('new', views.new),
    path('create', views.create),
    path('view/<int:id>', views.view),
    path('edit/<int:id>', views.edit),
    path('update/<int:id>', views.update),
    path('delete/<int:id>', views.delete),
    path('logout', views.logout),
]