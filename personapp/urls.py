from django.urls import path
from . import views

app_name = 'personapp'

urlpatterns = [
    path('personList/', views.PersonListView.as_view(), name='personList'),
    path('personInsert/', views.PersonInsertView.as_view(), name='personInsert'),
    path('personEdit/<pk>/', views.PersonEditView.as_view(), name='personEdit'),
]
