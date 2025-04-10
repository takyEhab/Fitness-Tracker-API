from rest_framework import generics, permissions
from .models import Activity
from .serializers import ActivitySerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination



#pagination
class ActivityHistoryPagination(PageNumberPagination):
    page_size = 10  # Customize number of items per page
    page_size_query_param = 'page_size'  
    max_page_size = 100  


#custom permission
class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class ActivityListCreateView(generics.ListCreateAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ActivityRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # User can only access their own data
        return self.request.user


class ActivityHistoryView(generics.ListAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ActivityHistoryPagination

    def get_queryset(self):
        user = self.request.user
        queryset = Activity.objects.filter(user=user)

        # Filters
        activity_type = self.request.query_params.get('activity_type')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if activity_type:
            queryset = queryset.filter(activity_type__iexact=activity_type)

        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        elif start_date:
            queryset = queryset.filter(date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(date__lte=end_date)

        # Sorting
        sort_by = self.request.query_params.get('sort_by', 'date')  # Default to sorting by 'date'
        if sort_by in ['date', 'duration', 'calories_burned']:
            queryset = queryset.order_by(sort_by)

        return queryset

class ActivityMetricsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        activities = Activity.objects.filter(user=user)

        if start_date:
            activities = activities.filter(date__gte=start_date)
        if end_date:
            activities = activities.filter(date__lte=end_date)

        total_duration = activities.aggregate(Sum('duration'))['duration__sum'] or 0
        total_calories = activities.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0

        return Response({
            "total_duration": total_duration,
            "total_calories": total_calories,
        })
