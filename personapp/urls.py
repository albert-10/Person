from django.urls import path
from . import views

app_name = 'personapp'

urlpatterns = [
    path('personList/', views.PersonListView.as_view(), name='personList'),   
]
