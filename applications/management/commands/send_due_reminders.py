from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone
from applications.models import Reminder

class Command(BaseCommand):
    help = "Send due reminders that have not already been sent."

    def handle(self, *args, **options):
        now = timezone.now()
        sent_count = 0
        # SQLite is fine for a single local worker. Use PostgreSQL row locks for
        # safe concurrent workers in production.
        due_ids = list(Reminder.objects.filter(sent_at__isnull=True, due_at__lte=now)
                       .values_list("id", flat=True).order_by("due_at")[:500])
        for reminder_id in due_ids:
            with transaction.atomic():
                reminder = Reminder.objects.select_for_update().select_related(
                    "application__user"
                ).filter(id=reminder_id, sent_at__isnull=True, due_at__lte=now).first()
                if not reminder:
                    continue
                user = reminder.application.user
                if not user.email:
                    self.stderr.write(f"Skipping reminder {reminder.id}: user has no email")
                    continue
                send_mail(
                    subject=f"Job application reminder: {reminder.application.company}",
                    message=reminder.message,
                    from_email=None,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                reminder.sent_at = timezone.now()
                reminder.save(update_fields=["sent_at"])
                sent_count += 1
        self.stdout.write(self.style.SUCCESS(f"Sent {sent_count} reminder(s)."))
