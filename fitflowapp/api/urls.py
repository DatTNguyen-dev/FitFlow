"""
URL routing for FitFlow API
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from fitflowapp.views import (
    UserProfileViewSet, FitnessGoalViewSet, PersonalScheduleViewSet,
    ExercisePlanViewSet, WorkoutScheduleViewSet, WorkoutSessionViewSet,
    BodyMetricsViewSet, ProgressReportViewSet, NotificationViewSet
)

# Tạo router
router = DefaultRouter()

# Đăng ký viewsets
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'goals', FitnessGoalViewSet, basename='goal')
router.register(r'schedules/personal', PersonalScheduleViewSet, basename='personal-schedule')
router.register(r'plans/exercise', ExercisePlanViewSet, basename='exercise-plan')
router.register(r'schedules/workout', WorkoutScheduleViewSet, basename='workout-schedule')
router.register(r'sessions', WorkoutSessionViewSet, basename='workout-session')
router.register(r'metrics', BodyMetricsViewSet, basename='body-metrics')
router.register(r'reports', ProgressReportViewSet, basename='progress-report')
router.register(r'notifications', NotificationViewSet, basename='notification')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
]
