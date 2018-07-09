from django.contrib import admin

from .models import Sessions, KeyEvents, SerialFrames, TestSubjects

# Register your models here.

admin.site.register(Sessions)
admin.site.register(KeyEvents)
admin.site.register(SerialFrames)
admin.site.register(TestSubjects)
