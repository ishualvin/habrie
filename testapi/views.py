from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FileUploadParser

import csv
from io import TextIOWrapper
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings

from .serializers import *
from .models import *



# Create your views here.

class AcademicDetailAPIView(APIView):
    def post(self, request):
        try:
            serializer = AcademicDetailsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


class ParentAPIView(APIView):
    def post(self, request):
        try:
            serializer = ParentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


class StudentAPIView(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


class DocumentAPIView(APIView):
    def get(self, request, format=None):
        documents = Document.objects.all()
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BulkImportAPIView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        try:
            file = request.data['file']
            csv_file = TextIOWrapper(file, encoding=request.encoding)
            reader = csv.DictReader(csv_file)
            students = []
            for row in reader:
                student_data = {
                    'student_name': row['student_name'],
                    'gender': row['gender'],
                    'adhar_card_number': row['adhar_card_number'],
                    'dob': row['dob'],
                    'identification_marks': row['identification_marks'],
                    'admission_category': row['admission_category'],
                    'height': row['height'],
                    'weight': row['weight'],
                    'email': row['email'],
                    'contact_detail': row['contact_detail'],
                    'address': row['address'],
                }

                # Create student serializer and validate
                student_serializer = StudentSerializer(data=student_data)
                if student_serializer.is_valid():
                    student = student_serializer.save()
                    students.append(student)
                else:
                    return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                academic_details_data = {
                    'student': student.id,  # Set the student foreign key
                    'class_name': row['class_name'],
                    'section': row['section'],
                    'date_of_joining': row['date_of_joining'],
                }
                parent_data = {
                    'student': student.id,  # Set the student foreign key
                    'father_name': row['father_name'],
                    'father_qualification': row['father_qualification'],
                    'father_profession': row['father_profession'],
                    'father_designation': row['father_designation'],
                    'father_mobile_number': row['father_mobile_number'],
                    'father_email': row['father_email'],
                    'mother_name': row['mother_name'],
                    'mother_qualification': row['mother_qualification'],
                    'mother_profession': row['mother_profession'],
                    'mother_designation': row['mother_designation'],
                    'mother_mobile_number': row['mother_mobile_number'],
                    'mother_email': row['mother_email'],
                }

                academic_details_serializer = AcademicDetailsSerializer(data=academic_details_data)
                if academic_details_serializer.is_valid():
                    academic_details_serializer.save(student=student)
                else:
                    return Response(academic_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                parent_serializer = ParentSerializer(data=parent_data)
                if parent_serializer.is_valid():
                    parent_serializer.save(student=student)
                else:
                    return Response(parent_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response("Data imported successfully", status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(f"An error occurred during import: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentFilterAPIView(APIView):

    def get(self, request):
        try:
            # Get the filter parameters from the request
            class_name = request.GET.get('class_name')
            session = request.GET.get('session')
            section = request.GET.get('section')
            admission_category = request.GET.get('admission_category')
            
            # Filter the students based on the provided parameters
            students = Student.objects.all()

            if class_name:
                students = students.filter(academic_details__class_name=class_name)
            if session:
                students = students.filter(academic_details__date_of_joining=session)
            if section:
                students = students.filter(academic_details__section=section)
            if admission_category:
                students = students.filter(admission_category=admission_category)
            
            # Check if any students match the filters
            if not students.exists():
                error_message = 'No students found with the provided filters.'
                return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)

            # Serialize the filtered students
            serializer = StudentSerializer(students, many=True)
            serialized_data = serializer.data
            
            # Generate a PDF using reportlab
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="student_data.pdf"'

            # Create a PDF canvas
            pdf_canvas = canvas.Canvas(response)

            # Iterate over each student
            for student in students:
                # Write the details of each student to the PDF
                pdf_canvas.drawString(100, 100, f"Student Name: {student.student_name}")
                pdf_canvas.drawString(100, 120, f"Gender: {student.gender}")
                pdf_canvas.drawString(100, 140, f"Adhar Card Number: {student.adhar_card_number}")
                pdf_canvas.drawString(100, 160, f"Date of Birth: {student.dob}")
                pdf_canvas.drawString(100, 180, f"Identification Marks: {student.identification_marks}")
                pdf_canvas.drawString(100, 200, f"Admission Category: {student.admission_category}")
                pdf_canvas.drawString(100, 220, f"Height: {student.height}")
                pdf_canvas.drawString(100, 240, f"Weight: {student.weight}")
                pdf_canvas.drawString(100, 260, f"Email: {student.email}")
                pdf_canvas.drawString(100, 280, f"Contact Detail: {student.contact_detail}")
                pdf_canvas.drawString(100, 300, f"Address: {student.address}")

                # Access and write the academic details of each student to the PDF
                academic_details = student.academic_details.first()
                pdf_canvas.drawString(100, 320, f"Class Name: {academic_details.class_name}")
                pdf_canvas.drawString(100, 340, f"Date of Joining: {academic_details.date_of_joining}")
                pdf_canvas.drawString(100, 360, f"Section: {academic_details.section}")

                pdf_canvas.showPage()

            # Save the PDF content
            pdf_canvas.save()
            return response
        except Exception as e:
            error_message = str(e)
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)


class MailAPIView(APIView):
    def post(self, request):
        try:
            serializer = AcademicDetailsSerializer(data=request.data)
            if serializer.is_valid():
                # Save the academic details
                academic_detail = serializer.save()

                # Send email to the student
                student_subject = "Enrollment Confirmation - Dummy School"
                student_message = f"Dear {academic_detail.student.student_name},\n\nYou have been enrolled in Dummy School. Your Enrollment ID is {academic_detail.enrollment_id}. Please provide us with the necessary hard documents for future reference.\n\nTeam\nDummy School"
                send_mail(student_subject, student_message, settings.DEFAULT_FROM_EMAIL, [academic_detail.student.email])

                # Send email notification to the admin
                admin_subject = "New Student Enrollment Notification - Dummy School"
                admin_message = f"Dear Admin,\n\nA new student, {academic_detail.student.student_name}, has been enrolled in class {academic_detail.class_name}, section {academic_detail.section} with Enrollment ID {academic_detail.enrollment_id} for the {academic_detail.date_of_joining} session."
                send_mail(admin_subject, admin_message, settings.DEFAULT_FROM_EMAIL, ['durganand.jha@habrie.com'])

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_message = str(e)
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)