from django.urls import path

from . import views


urlpatterns = [
    path('', views.InventoryListCreateAPIView.as_view()),
    path('<id>/', views.InventoryRetreiveUpdateAPIView.as_view()),
]
