from django.conf import settings
from django.db import models
from django.utils import timezone

class Application(models.Model):
    class Status(models.TextChoices):
        SAVED = "saved", "Saved"
        APPLIED = "applied", "Applied"
        SCREENING = "screening", "Screening"
        INTERVIEW = "interview", "Interview"
        OFFER = "offer", "Offer"
        REJECTED = "rejected", "Rejected"
        WITHDRAWN = "withdrawn", "Withdrawn"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    company = models.CharField(max_length=160)
    role = models.CharField(max_length=160)
    location = models.CharField(max_length=160, blank=True)
    job_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SAVED)
    applied_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["user", "status", "applied_at"], name="app_user_status_date"),
            models.Index(fields=["user", "updated_at"], name="app_user_updated"),
        ]

    def __str__(self):
        return f"{self.role} at {self.company}"

class Interview(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="interviews")
    scheduled_at = models.DateTimeField()
    interview_type = models.CharField(max_length=80, blank=True)
    interviewer = models.CharField(max_length=160, blank=True)
    location_or_link = models.CharField(max_length=500, blank=True)
    outcome = models.CharField(max_length=80, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["application", "scheduled_at"], name="int_app_schedule")]

class Note(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="notes")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["application", "created_at"], name="note_app_created")]

class Reminder(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="reminders")
    due_at = models.DateTimeField()
    message = models.CharField(max_length=300)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["due_at", "sent_at"], name="rem_due_sent")]

    @property
    def is_sent(self):
        return self.sent_at is not None
