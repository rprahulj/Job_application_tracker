from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from applications.views import (
    RegisterView, ApplicationViewSet, InterviewViewSet, NoteViewSet,
    ReminderViewSet, StatsView,
)

router = DefaultRouter()
router.register("applications", ApplicationViewSet, basename="application")
router.register("interviews", InterviewViewSet, basename="interview")
router.register("notes", NoteViewSet, basename="note")
router.register("reminders", ReminderViewSet, basename="reminder")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/stats/", StatsView.as_view(), name="stats"),
    path("api/", include(router.urls)),
]
