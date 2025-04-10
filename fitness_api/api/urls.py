from django.urls import path
from .views import ActivityListCreateView, ActivityRetrieveUpdateDestroyView, ActivityHistoryView, ActivityMetricsView

urlpatterns = [
    path('activities/', ActivityListCreateView.as_view(), name='activity-list'),
    path('activities/<int:pk>/', ActivityRetrieveUpdateDestroyView.as_view(), name='activity-detail'),
    
    path('activities/metrics/', ActivityMetricsView.as_view(), name='activity-metrics'),
    path('activities/history/', ActivityHistoryView.as_view(), name='activity-history'),
]
