import re, random
from django.db import models
from datetime import datetime

# Create your models here.


class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    student_name = models.CharField(max_length=100, null=False, blank=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    adhar_card_number = models.CharField(max_length=12, default="0")
    dob = models.DateField(max_length=8)
    identification_marks = models.TextField()
    admission_category = models.CharField(max_length=100, null=False, blank=False)
    height = models.FloatField(blank=False, null=False)
    weight = models.FloatField(blank=False, null=False)
    email = models.EmailField(max_length=70, blank=True, null=True)
    contact_detail = models.CharField(max_length=12, blank=False, null=False)
    address = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.student_name


class Parent(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=100, null=False, blank=False)
    father_qualification = models.CharField(max_length=100, null=False, blank=False)
    father_profession = models.CharField(max_length=100, null=False, blank=False)
    father_designation = models.CharField(max_length=100, null=False, blank=False)
    father_aadhar_card = models.CharField(max_length=12, default="0")
    father_mobile_number =  models.CharField(max_length=12, blank=False, null=False)
    father_email = models.EmailField(max_length=70, blank=True, null=True)
    
    mother_name = models.CharField(max_length=100, null=False, blank=False)
    mother_qualification = models.CharField(max_length=100, null=False, blank=False)
    mother_profession = models.CharField(max_length=100, null=False, blank=False)
    mother_designation = models.CharField(max_length=100, null=False, blank=False)
    mother_aadhar_card = models.CharField(max_length=12, default="0")
    mother_mobile_number = models.CharField(max_length=12, blank=False, null=False)
    mother_email = models.EmailField(max_length=70, blank=True, null=True)

    def __str__(self):
        return f"Parent of {self.student}"



class Academic_Detail(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=100, null=False, blank=False)
    section = models.CharField(max_length=100, null=False, blank=False)
    date_of_joining = models.DateField()

    def generate_enrollment_id(self):
        # Generate the first 6 digits based on the enrollment date
        date_part = datetime.now().strftime('%d%m%y')

        # Generate the three letters from the student name
        name_part = re.sub('[^a-zA-Z]', '', self.student.student_name)[:3].lower()

        # Generate the last 3 digits as a random number between 001 and 999
        random_part = str(random.randint(1, 999)).zfill(3)

        # Concatenate the parts to form the enrollment ID
        enrollment_id = f'{date_part}{name_part}{random_part}'
        print('>>><<', enrollment_id)
        
        return enrollment_id

    def save(self, *args, **kwargs):
        if not self.pk:
            self.enrollment_id = self.generate_enrollment_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Academic Details of {self.student}"



class Document(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    document_file = models.FileField(upload_to='documents/')
    
    def __str__(self):
        return f"Document of {self.student}"
    