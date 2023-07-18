from django.urls import path
from .views import *

urlpatterns = [
    path('student/', StudentCreateView.as_view(), name='student-create'),
    path('student-list/',StudentListView.as_view(), name='student-list'),
    path('bulk-import/', BulkImportView.as_view()),
    path('parent/', ParentCreateView.as_view(), name='parent-create'),
    path('parent-list/',ParentListView.as_view(), name='parent-list'),
    path('academic-details/', AcademicDetailsCreateView.as_view(), name='academic-details-create'),
    path('academic-details-list/', AcademicDetailsListView.as_view(), name='academic-details-list'),
    path('document-upload/', DocumentUploadCreateView.as_view(), name='document-upload-create'),
    path('document-list/', DocumentListView.as_view(), name='document-list'),
    
    path('student-filter/', StudentFilterView.as_view(), name='student-filter'),
    path('students/export/excel/', StudentExportExcelView.as_view()),
    path('students/export/pdf/', StudentExportPDFView.as_view()),
    path('mail/', FinalSubmitView.as_view(), name='mail')
]
