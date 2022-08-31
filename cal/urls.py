from os import path
# cal/urls.py
from . import views
from django.urls import path

app_name = 'cal'

urlpatterns = [
    path('', views.CalView, name='home'),
    path('<int:year>/<int:month>', views.CalView, name='home'),
    path('addevent/', views.addCalEvent, name='add-cal-event'),
]
