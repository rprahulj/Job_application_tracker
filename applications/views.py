from datetime import timedelta
from django.db.models import Count
from django.db.models.functions import TruncWeek
from django.utils import timezone
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Application, Interview, Note, Reminder
from .serializers import (
    RegisterSerializer, ApplicationSerializer, InterviewSerializer,
    NoteSerializer, ReminderSerializer,
)
from .permissions import IsOwnerOfApplicationRelatedObject

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class OwnedQuerysetMixin:
    permission_classes = [IsAuthenticated, IsOwnerOfApplicationRelatedObject]
    def perform_create(self, serializer):
        # Ownership is never accepted from request JSON.
        serializer.save(application=self.request.user.applications.get(pk=self.request.data.get("application"))) if self.related_to_application else serializer.save(user=self.request.user)

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["company", "role", "location", "description"]
    ordering_fields = ["applied_at", "company", "updated_at"]
    ordering = ["-updated_at"]
    def get_queryset(self):
        qs = Application.objects.filter(user=self.request.user)
        status = self.request.query_params.get("status")
        company = self.request.query_params.get("company")
        if status:
            qs = qs.filter(status=status)
        if company:
            qs = qs.filter(company__icontains=company)
        return qs
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class InterviewViewSet(viewsets.ModelViewSet):
    serializer_class = InterviewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOfApplicationRelatedObject]
    def get_queryset(self):
        return Interview.objects.filter(application__user=self.request.user).select_related("application")
    def perform_create(self, serializer):
        app = self.request.user.applications.get(pk=self.request.data.get("application"))
        serializer.save(application=app)

class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsOwnerOfApplicationRelatedObject]
    def get_queryset(self):
        return Note.objects.filter(application__user=self.request.user).select_related("application")
    def perform_create(self, serializer):
        app = self.request.user.applications.get(pk=self.request.data.get("application"))
        serializer.save(application=app)

class ReminderViewSet(viewsets.ModelViewSet):
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOfApplicationRelatedObject]
    def get_queryset(self):
        return Reminder.objects.filter(application__user=self.request.user).select_related("application")
    def perform_create(self, serializer):
        app = self.request.user.applications.get(pk=self.request.data.get("application"))
        serializer.save(application=app)

class StatsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        owned = Application.objects.filter(user=request.user)
        by_status = list(owned.values("status").annotate(count=Count("id")).order_by("status"))
        weekly = list(
            owned.exclude(applied_at__isnull=True)
            .annotate(week=TruncWeek("applied_at"))
            .values("week").annotate(count=Count("id")).order_by("week")
        )
        return Response({
            "total": owned.count(),
            "by_status": by_status,
            "weekly_applications": [
                {"week": row["week"].date().isoformat() if row["week"] else None, "count": row["count"]}
                for row in weekly
            ],
        })
