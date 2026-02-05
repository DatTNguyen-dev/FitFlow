"""
Views for FitFlow API
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .models import (
    UserProfile, FitnessGoal, PersonalSchedule, ExercisePlan,
    WorkoutSchedule, WorkoutSession, ExerciseLog, BodyMetrics,
    ProgressReport, Notification, ConstraintAndPreference
)
from .serializers import (
    UserProfileSerializer, FitnessGoalSerializer, PersonalScheduleSerializer,
    ExercisePlanSerializer, WorkoutScheduleSerializer, WorkoutSessionSerializer,
    BodyMetricsSerializer, ProgressReportSerializer, NotificationSerializer
)

class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet cho User Profile"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

class FitnessGoalViewSet(viewsets.ModelViewSet):
    """ViewSet cho Fitness Goal"""
    permission_classes = [IsAuthenticated]
    serializer_class = FitnessGoalSerializer
    
    def get_queryset(self):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        return FitnessGoal.objects.filter(user_profile=user_profile)


class PersonalScheduleViewSet(viewsets.ModelViewSet):
    """ViewSet cho Personal Schedule"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        return PersonalSchedule.objects.filter(user_profile=user_profile)


class ExercisePlanViewSet(viewsets.ModelViewSet):
    """ViewSet cho Exercise Plan"""
    permission_classes = [IsAuthenticated]
    serializer_class = ExercisePlanSerializer
    
    def get_queryset(self):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        return ExercisePlan.objects.filter(user_profile=user_profile)
    
    @action(detail=False, methods=['post'])
    def generate_plan(self, request):
        """Tạo kế hoạch tập luyện bằng agent"""
        try:
            from .agents_config.agent_manager import agent_manager
            if agent_manager is None:
                return Response(
                    {'error': 'Agent manager not initialized'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            user_profile = get_object_or_404(UserProfile, user=request.user)
            
            # Chuẩn bị dữ liệu input
            user_input = {
                'user_id': user_profile.id,
                'current_level': user_profile.current_level,
                'age': user_profile.age,
                'weight_kg': user_profile.weight_kg,
                'height_cm': user_profile.height_cm,
            }
            
            # Thêm goal info nếu có
            if hasattr(user_profile, 'fitness_goal'):
                goal = user_profile.fitness_goal
                user_input.update({
                    'goal': goal.primary_goal,
                    'hours_per_week': goal.hours_per_week,
                    'target_date': goal.target_date.isoformat() if goal.target_date else None,
                })
            
            # Gọi Planning Agent
            response = agent_manager.process_request(user_input, agent_type='planning')
            
            # Lưu kế hoạch
            exercise_plan, created = ExercisePlan.objects.get_or_create(
                user_profile=user_profile
            )
            exercise_plan.plan_data = response
            exercise_plan.save()
            
            return Response(response, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class WorkoutScheduleViewSet(viewsets.ModelViewSet):
    """ViewSet cho Workout Schedule"""
    permission_classes = [IsAuthenticated]
    serializer_class = WorkoutScheduleSerializer
    
    def get_queryset(self):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        return WorkoutSchedule.objects.filter(user_profile=user_profile)
    
    @action(detail=False, methods=['post'])
    def generate_schedule(self, request):
        """Tạo lịch tập luyện bằng agent"""
        try:
            from .agents_config.agent_manager import agent_manager
            if agent_manager is None:
                return Response(
                    {'error': 'Agent manager not initialized'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            user_profile = get_object_or_404(UserProfile, user=self.request.user)
            
            # Lấy exercise plan
            try:
                exercise_plan = ExercisePlan.objects.get(user_profile=user_profile)
            except ExercisePlan.DoesNotExist:
                return Response(
                    {'error': 'No exercise plan found. Please generate a plan first.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Lấy personal schedule
            personal_schedules = PersonalSchedule.objects.filter(user_profile=user_profile)
            personal_timetable = {
                schedule.day: {
                    'start_time': str(schedule.start_time),
                    'end_time': str(schedule.end_time),
                    'available': schedule.available,
                } for schedule in personal_schedules
            }
            
            # Chuẩn bị input
            user_input = {
                'user_id': user_profile.id,
                'exercise_plan': exercise_plan.plan_data,
                'personal_timetable': personal_timetable,
                'preferences': {
                    'preferred_times': request.data.get('preferred_times', ['morning', 'afternoon']),
                    'location': getattr(user_profile.constraints_preferences, 'preferred_location', 'gym'),
                }
            }
            
            # Gọi Schedule Agent
            response = agent_manager.process_request(user_input, agent_type='schedule')
            
            # Lưu schedule
            workout_schedule, created = WorkoutSchedule.objects.get_or_create(
                user_profile=user_profile
            )
            workout_schedule.schedule_data = response
            workout_schedule.save()
            
            return Response(response, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class WorkoutSessionViewSet(viewsets.ModelViewSet):
    """ViewSet cho Workout Session"""
    permission_classes = [IsAuthenticated]
    serializer_class = WorkoutSessionSerializer
    
    def get_queryset(self):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        return WorkoutSession.objects.filter(user_profile=user_profile)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Lấy các workout sắp tới"""
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        today = timezone.now().date()
        
        sessions = WorkoutSession.objects.filter(
            user_profile=user_profile,
            scheduled_date__gte=today,
            status__in=['planned', 'in_progress']
        ).order_by('scheduled_date', 'scheduled_time')
        
        return Response([
            {
                'id': s.pk,  # Use pk instead of id
                'scheduled_date': s.scheduled_date,
                'scheduled_time': s.scheduled_time,
                'status': s.status,
            } for s in sessions
        ])
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """Lấy lịch sử workout"""
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        sessions = WorkoutSession.objects.filter(
            user_profile=user_profile,
            status__in=['completed', 'skipped']
        ).order_by('-scheduled_date')
        
        return Response([
            {
                'id': s.id,
                'scheduled_date': s.scheduled_date,
                'status': s.status,
            } for s in sessions
        ])


class BodyMetricsViewSet(viewsets.ModelViewSet):
    """ViewSet cho Body Metrics"""
    permission_classes = [IsAuthenticated]
    serializer_class = BodyMetricsSerializer
    
    def get_queryset(self):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        return BodyMetrics.objects.filter(user_profile=user_profile)
    
    def perform_create(self, serializer):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        serializer.save(user_profile=user_profile)


class ProgressReportViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet cho Progress Report"""
    permission_classes = [IsAuthenticated]
    serializer_class = ProgressReportSerializer
    
    def get_queryset(self):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        return ProgressReport.objects.filter(user_profile=user_profile)
    
    @action(detail=False, methods=['post'])
    def generate_report(self, request):
        """Tạo báo cáo tiến độ bằng agent"""
        try:
            from .agents_config.agent_manager import agent_manager
            if agent_manager is None:
                return Response(
                    {'error': 'Agent manager not initialized'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            user_profile = get_object_or_404(UserProfile, user=request.user)
            
            report_type = request.data.get('report_type', 'weekly')
            
            # Tính toán thời gian
            today = timezone.now().date()
            if report_type == 'weekly':
                start_date = today - timedelta(days=7)
                end_date = today
            elif report_type == 'monthly':
                start_date = today - timedelta(days=30)
                end_date = today
            else:
                # support custom range via start_date / end_date ISO strings
                start_str = request.data.get('start_date')
                end_str = request.data.get('end_date')
                try:
                    start_date = datetime.fromisoformat(start_str).date() if start_str else (today - timedelta(days=7))
                    end_date = datetime.fromisoformat(end_str).date() if end_str else today
                except Exception:
                    return Response({'error': 'Invalid date format for start_date or end_date'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Lấy dữ liệu
            sessions_qs = WorkoutSession.objects.filter(
                user_profile=user_profile,
                scheduled_date__range=(start_date, end_date)
            ).order_by('scheduled_date')
            sessions = [
                {
                    'id': s.pk,
                    'scheduled_date': str(s.scheduled_date),
                    'scheduled_time': str(s.scheduled_time) if hasattr(s, 'scheduled_time') else None,
                    'status': s.status,
                } for s in sessions_qs
            ]
            
            metrics_qs = BodyMetrics.objects.filter(
                user_profile=user_profile,
            )
            # attempt to filter metrics by date fields if present
            try:
                metrics_qs = metrics_qs.filter(recorded_at__date__range=(start_date, end_date))
            except Exception:
                pass
            metrics = list(metrics_qs.values())
            
            progress_qs = ProgressReport.objects.filter(
                user_profile=user_profile,
            )
            try:
                progress_qs = progress_qs.filter(created_at__date__range=(start_date, end_date))
            except Exception:
                pass
            existing_reports = list(progress_qs.values())
            
            user_input = {
                'user_id': user_profile.id,
                'report_type': report_type,
                'start_date': str(start_date),
                'end_date': str(end_date),
                'sessions': sessions,
                'body_metrics': metrics,
                'existing_reports': existing_reports,
            }
            
            # Gọi Tracking/Master Agent để tạo báo cáo
            response = agent_manager.process_request(user_input, agent_type='tracking')
            
            # Lưu ProgressReport (tùy thuộc model của bạn)
            try:
                report_obj = ProgressReport.objects.create(
                    user_profile=user_profile,
                    report_type=report_type,
                    report_data=response
                )
                serializer = ProgressReportSerializer(report_obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception:
                # Nếu không thể lưu, trả về response từ agent trực tiếp
                return Response(response, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet cho Notification"""
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        return Notification.objects.filter(user_profile=user_profile)
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Lấy các thông báo chưa đọc"""
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        notifications = Notification.objects.filter(
            user_profile=user_profile,
            read=False
        ).order_by('-created_at')
        
        return Response([
            {
                'id': n.id,
                'title': n.title,
                'message': n.message,
                'type': n.notification_type,
            } for n in notifications
        ])
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Đánh dấu tất cả thông báo là đã đọc"""
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        Notification.objects.filter(
            user_profile=user_profile,
            read=False
        ).update(read=True)
        
        return Response({'status': 'All notifications marked as read'})