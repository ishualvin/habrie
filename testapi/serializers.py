from rest_framework import serializers, pagination
from .models import *


#Academic Serializer
class AcademicDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Academic_Detail
        fields = '__all__'

    def create(self, validated_data):
        # Check if a user with the same details already exists
        existing_user = Academic_Detail.objects.filter(**validated_data).first()
        if existing_user:
            raise serializers.ValidationError('Academic Detail already exists.')

        # If no existing user found, create a new one
        return super().create(validated_data)


#Parent Serializer
class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'

    def create(self, validated_data):
        # Check if a user with the same details already exists
        existing_user = Parent.objects.filter(**validated_data).first()
        if existing_user:
            raise serializers.ValidationError('Parent already exists.')

        # If no existing user found, create a new one
        return super().create(validated_data)
    
    def validate_father_mobile_number(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Father mobile number should be a 10-digit numeric value.")
        return value

    def validate_mother_mobile_number(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Mother mobile number should be a 10-digit numeric value.")
        return value
    
    def validate_adhar(self, value):
        if not value.isdigit() or len(value) != 12:
            raise serializers.ValidationError("Adhar detail should be a 12-digit numeric value.")
        return value


#Student Serializer
class StudentSerializer(serializers.ModelSerializer):
    academic_details = AcademicDetailsSerializer(many=True, read_only=True)
    parent = ParentSerializer(read_only=True)
    
    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        # Check if a user with the same details already exists
        existing_user = Student.objects.filter(**validated_data).first()
        if existing_user:
            raise serializers.ValidationError('Student Detail already exists.')

        # If no existing user found, create a new one
        return super().create(validated_data)
    
    def validate_student_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Student name must be at least 2 characters long.")
        return value

    def validate_contact_detail(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Contact detail should be a 10-digit numeric value.")
        return value

    def validate_adhar(self, value):
        if not value.isdigit() or len(value) != 12:
            raise serializers.ValidationError("Adhar detail should be a 12-digit numeric value.")
        return value


#Document Upload Serializer
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['document_file']

    def create(self, validated_data):
        # Check if a user with the same details already exists
        existing_user = Document.objects.filter(**validated_data).first()
        if existing_user:
            raise serializers.ValidationError('Document already exists.')

        # If no existing user found, create a new one
        return super().create(validated_data)


class StudentResultsPagination(pagination.PageNumberPagination):
    page_size =10 # how much students detail display per page
    page_size_query_param = 'page_size'
    max_page_size = 10000