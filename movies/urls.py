from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home_page'), # if someone go to yourapp.com it tells to run home_page function
    path('create/', views.create, name='create'),  # so if somebody go to yourapp.com/create it will run the create function.
    path('edit/<str:movie_id>', views.edit, name='edit'), # so if somebody go to yourapp.com/edit/rec55456 then it will mrun/trigger that edit                                                                     function in views.py
    path('delete/<str:movie_id>', views.delete, name='delete'),
]
