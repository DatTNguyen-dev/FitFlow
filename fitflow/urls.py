"""
URL configuration for fitflow project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from fitflowapp.views import (
    UserProfileViewSet, FitnessGoalViewSet, PersonalScheduleViewSet,
    ExercisePlanViewSet, WorkoutScheduleViewSet, WorkoutSessionViewSet,
    BodyMetricsViewSet, ProgressReportViewSet
)

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'user-profiles', UserProfileViewSet, basename='userprofile')
router.register(r'fitness-goals', FitnessGoalViewSet, basename='fitnessgoal')
router.register(r'personal-schedules', PersonalScheduleViewSet, basename='personalschedule')
router.register(r'exercise-plans', ExercisePlanViewSet, basename='exerciseplan')
router.register(r'workout-schedules', WorkoutScheduleViewSet, basename='workoutschedule')
router.register(r'workout-sessions', WorkoutSessionViewSet, basename='workoutsession')
router.register(r'body-metrics', BodyMetricsViewSet, basename='bodymetrics')
router.register(r'progress-reports', ProgressReportViewSet, basename='progressreport')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),
]
