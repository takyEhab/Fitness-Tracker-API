from django.urls import path
from .views import ActivityListCreateView, ActivityRetrieveUpdateDestroyView

urlpatterns = [
    path('activities/', ActivityListCreateView.as_view(), name='activity-list'),
    path('activities/<int:pk>/', ActivityRetrieveUpdateDestroyView.as_view(), name='activity-detail'),
]
