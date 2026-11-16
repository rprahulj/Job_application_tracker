from django.contrib import admin
from .models import Application, Interview, Note, Reminder
admin.site.register(Application)
admin.site.register(Interview)
admin.site.register(Note)
admin.site.register(Reminder)
