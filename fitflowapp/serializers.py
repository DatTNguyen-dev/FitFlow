"""
Serializers for FitFlow API
"""
from rest_framework import serializers
from .models import (
    UserProfile, FitnessGoal, PersonalSchedule, ExercisePlan,
    WorkoutSchedule, WorkoutSession, ExerciseLog, BodyMetrics,
    ProgressReport, Notification
)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class FitnessGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessGoal
        fields = '__all__'


class PersonalScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalSchedule
        fields = '__all__'


class ExercisePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExercisePlan
        fields = '__all__'


class WorkoutScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutSchedule
        fields = '__all__'


class WorkoutSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutSession
        fields = '__all__'


class BodyMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyMetrics
        fields = '__all__'


class ProgressReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressReport
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
