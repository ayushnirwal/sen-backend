from django.contrib import admin
from .models import Prof,LecInstances,AttendanceRecord,ValidTokens,Code

# Register your models here.
admin.site.register(Prof)
admin.site.register(LecInstances)
admin.site.register(AttendanceRecord)
admin.site.register(ValidTokens)
admin.site.register(Code)