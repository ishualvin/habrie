from celery import shared_task
from .views import perform_import


@shared_task
def import_data_async(file_path):
    # Call the perform_import function from your view
    perform_import(file_path)