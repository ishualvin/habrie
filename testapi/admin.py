from django.contrib import admin
from .models import *

# Register your models here.

class Academic_DetailAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_name', 'section', 'date_of_joining', 'get_enrollment_id')

    def get_enrollment_id(self, obj):
        return obj.generate_enrollment_id()
    get_enrollment_id.short_description = 'Enrollment ID'

admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Academic_Detail, Academic_DetailAdmin)
admin.site.register(Document)