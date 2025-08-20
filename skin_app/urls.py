from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_skin_disease, name='predict_skin_disease'),
]
