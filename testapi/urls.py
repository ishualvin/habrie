from django.urls import path
from .views import *

urlpatterns = [
    path('students/', StudentAPIView.as_view(), name='student-api'),
    path('academic-details/', AcademicDetailAPIView.as_view(), name='academic-details-api'),
    path('parents/', ParentAPIView.as_view(), name='parent-api'),
    path('document-upload/', DocumentAPIView.as_view(), name='document-api'),
    path('bulk-import/', BulkImportAPIView.as_view()),
    path('student-filter/', StudentFilterAPIView.as_view(), name='student-filter'),
    path('mail/', MailAPIView.as_view(), name='mail')
]
