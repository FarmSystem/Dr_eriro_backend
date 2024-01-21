from django.contrib import admin
from .models import Doctor, Hospital, Subject

admin.site.register(Doctor)
admin.site.register(Hospital)
admin.site.register(Subject)