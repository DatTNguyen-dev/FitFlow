"""
Django Admin Configuration for FitFlow
"""
from django.contrib import admin
from .models import (
    UserProfile, FitnessGoal, PersonalSchedule, ExercisePlan,
    WorkoutSchedule, WorkoutSession, ExerciseLog, BodyMetrics,
    ProgressReport, Notification, ConstraintAndPreference
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_level', 'age', 'weight_kg', 'height_cm', 'created_at')
    list_filter = ('current_level', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(FitnessGoal)
class FitnessGoalAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'primary_goal', 'hours_per_week', 'target_date')
    list_filter = ('primary_goal', 'target_date')
    search_fields = ('user_profile__user__username',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(PersonalSchedule)
class PersonalScheduleAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'day', 'start_time', 'end_time', 'available')
    list_filter = ('day', 'available')
    search_fields = ('user_profile__user__username',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ExercisePlan)
class ExercisePlanAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'created_at', 'updated_at')
    search_fields = ('user_profile__user__username',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(WorkoutSchedule)
class WorkoutScheduleAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'created_at', 'updated_at')
    search_fields = ('user_profile__user__username',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'scheduled_date', 'scheduled_time', 'status', 'duration_minutes')
    list_filter = ('status', 'scheduled_date')
    search_fields = ('user_profile__user__username',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ExerciseLog)
class ExerciseLogAdmin(admin.ModelAdmin):
    list_display = ('workout_session', 'exercise_name', 'actual_reps', 'actual_weight_kg', 'rpe', 'completed')
    list_filter = ('completed', 'created_at', 'rpe')
    search_fields = ('exercise_name', 'workout_session__user_profile__user__username')
    readonly_fields = ('created_at',)


@admin.register(BodyMetrics)
class BodyMetricsAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'measurement_date', 'weight_kg', 'body_fat_percentage')
    list_filter = ('measurement_date', 'injury_status')
    search_fields = ('user_profile__user__username',)
    readonly_fields = ('created_at',)


@admin.register(ProgressReport)
class ProgressReportAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'report_type', 'report_date', 'adherence_rate')
    list_filter = ('report_type', 'report_date')
    search_fields = ('user_profile__user__username',)
    readonly_fields = ('created_at',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'notification_type', 'title', 'scheduled_time', 'read')
    list_filter = ('notification_type', 'read', 'scheduled_time')
    search_fields = ('title', 'user_profile__user__username')
    readonly_fields = ('created_at', 'sent_time')


@admin.register(ConstraintAndPreference)
class ConstraintAndPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'preferred_location')
    search_fields = ('user_profile__user__username',)
    readonly_fields = ('updated_at',)


# Customize admin site
admin.site.site_header = "FitFlow Administration"
admin.site.site_title = "FitFlow Admin"
admin.site.index_title = "Welcome to FitFlow Admin Dashboard"
