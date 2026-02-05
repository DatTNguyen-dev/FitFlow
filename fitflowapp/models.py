from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(models.Model):
    """Hồ sơ người dùng"""
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='fitness_profile')
    current_level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    age = models.IntegerField()
    weight_kg = models.FloatField()
    height_cm = models.FloatField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __str__(self):
        return f"{self.user.username} - {self.current_level}"


class FitnessGoal(models.Model):
    """Mục tiêu fitness của người dùng"""
    GOAL_CHOICES = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('endurance', 'Endurance'),
        ('flexibility', 'Flexibility'),
    ]
    
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='fitness_goal')
    primary_goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
    hours_per_week = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(168)])
    target_weight_kg = models.FloatField(null=True, blank=True)
    target_body_fat = models.FloatField(null=True, blank=True)
    start_date = models.DateField(auto_now_add=True)
    target_date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Fitness Goal"
        verbose_name_plural = "Fitness Goals"
    
    def __str__(self):
        return f"{self.user_profile.user.username} - {self.primary_goal}"


class PersonalSchedule(models.Model):
    """Lịch cá nhân của người dùng"""
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='personal_schedules')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    available = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Personal Schedule"
        verbose_name_plural = "Personal Schedules"
        unique_together = ['user_profile', 'day', 'start_time']
    
    def __str__(self):
        return f"{self.user_profile.user.username} - {self.day} {self.start_time}"


class ExercisePlan(models.Model):
    """Kế hoạch tập luyện"""
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='exercise_plan')
    plan_data = models.JSONField(default=dict)  # Lưu dữ liệu từ Planning Agent
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Exercise Plan"
        verbose_name_plural = "Exercise Plans"
    
    def __str__(self):
        return f"{self.user_profile.user.username} - Exercise Plan"


class WorkoutSchedule(models.Model):
    """Lịch tập luyện"""
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='workout_schedule')
    schedule_data = models.JSONField(default=dict)  # Lưu dữ liệu từ Schedule Agent
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Workout Schedule"
        verbose_name_plural = "Workout Schedules"
    
    def __str__(self):
        return f"{self.user_profile.user.username} - Workout Schedule"


class WorkoutSession(models.Model):
    """Phiên tập luyện"""
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('skipped', 'Skipped'),
    ]
    
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='workout_sessions')
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    
    exercises = models.JSONField(default=list)  # [ {"name": "...", "sets": X, "reps": Y, "weight": Z} ]
    duration_minutes = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Workout Session"
        verbose_name_plural = "Workout Sessions"
    
    def __str__(self):
        return f"{self.user_profile.user.username} - {self.scheduled_date}"


class ExerciseLog(models.Model):
    """Log chi tiết cho từng bài tập"""
    workout_session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name='exercise_logs')
    
    exercise_name = models.CharField(max_length=100)
    planned_sets = models.IntegerField()
    planned_reps = models.CharField(max_length=20)
    planned_weight_kg = models.FloatField()
    
    actual_sets = models.IntegerField()
    actual_reps = models.CharField(max_length=20)
    actual_weight_kg = models.FloatField()
    
    rpe = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True,
        blank=True,
        help_text="Rate of Perceived Exertion (1-10)"
    )
    notes = models.TextField(blank=True)
    
    completed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Exercise Log"
        verbose_name_plural = "Exercise Logs"
    
    def __str__(self):
        return f"{self.workout_session.user_profile.user.username} - {self.exercise_name}"


class BodyMetrics(models.Model):
    """Chỉ số cơ thể"""
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='body_metrics')
    
    measurement_date = models.DateField(auto_now_add=True)
    weight_kg = models.FloatField()
    body_fat_percentage = models.FloatField(null=True, blank=True)
    
    # Measurements
    chest_cm = models.FloatField(null=True, blank=True)
    arm_cm = models.FloatField(null=True, blank=True)
    waist_cm = models.FloatField(null=True, blank=True)
    thigh_cm = models.FloatField(null=True, blank=True)
    
    sleep_quality = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True,
        blank=True
    )
    energy_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True,
        blank=True
    )
    muscle_soreness = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True,
        blank=True
    )
    injury_status = models.CharField(
        max_length=20,
        choices=[
            ('none', 'None'),
            ('mild', 'Mild'),
            ('moderate', 'Moderate'),
            ('severe', 'Severe'),
        ],
        default='none'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Body Metrics"
        verbose_name_plural = "Body Metrics"
    
    def __str__(self):
        return f"{self.user_profile.user.username} - {self.measurement_date}"


class ProgressReport(models.Model):
    """Báo cáo tiến độ"""
    REPORT_TYPE_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom'),
    ]
    
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='progress_reports')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    
    report_date = models.DateField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    
    adherence_rate = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage of planned workouts completed"
    )
    
    performance_data = models.JSONField(default=dict)  # Dữ liệu hiệu suất chi tiết
    recommendations = models.JSONField(default=list)  # Danh sách đề xuất cải thiện
    
    report_summary = models.TextField()  # Tóm tắt báo cáo
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Progress Report"
        verbose_name_plural = "Progress Reports"
    
    def __str__(self):
        return f"{self.user_profile.user.username} - {self.report_type} Report ({self.report_date})"


class Notification(models.Model):
    """Thông báo nhắc nhở"""
    NOTIFICATION_TYPE_CHOICES = [
        ('reminder', 'Reminder'),
        ('achievement', 'Achievement'),
        ('alert', 'Alert'),
        ('update', 'Update'),
    ]
    
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    scheduled_time = models.DateTimeField()
    sent_time = models.DateTimeField(null=True, blank=True)
    read = models.BooleanField(default=False)
    
    related_workout_session = models.ForeignKey(
        WorkoutSession,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-scheduled_time']
    
    def __str__(self):
        return f"{self.user_profile.user.username} - {self.notification_type}"


class ConstraintAndPreference(models.Model):
    """Ràng buộc và sở thích của người dùng"""
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='constraints_preferences')
    
    injuries = models.JSONField(
        default=list,
        help_text="List of current or past injuries"
    )
    allergies = models.JSONField(default=list)
    mobility_issues = models.JSONField(default=list)
    
    preferred_exercises = models.JSONField(
        default=list,
        help_text="List of preferred exercises"
    )
    disliked_exercises = models.JSONField(
        default=list,
        help_text="List of exercises user dislikes"
    )
    
    available_equipment = models.JSONField(
        default=list,
        help_text="List of available equipment at home or gym"
    )
    
    preferred_workout_times = models.JSONField(
        default=list,
        help_text="Morning, Afternoon, Evening"
    )
    preferred_location = models.CharField(
        max_length=50,
        choices=[
            ('home', 'Home'),
            ('gym', 'Gym'),
            ('both', 'Both'),
        ],
        default='both'
    )
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Constraint and Preference"
        verbose_name_plural = "Constraints and Preferences"
    
    def __str__(self):
        return f"{self.user_profile.user.username} - Constraints & Preferences"
