# Generated by Django 4.2.3 on 2023-07-18 03:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('adhar_card_number', models.CharField(default='0', max_length=12)),
                ('dob', models.DateField(max_length=8)),
                ('identification_marks', models.TextField()),
                ('admission_category', models.CharField(max_length=100)),
                ('height', models.FloatField()),
                ('weight', models.FloatField()),
                ('email', models.EmailField(blank=True, max_length=70, null=True)),
                ('contact_detail', models.CharField(max_length=12)),
                ('address', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('father_name', models.CharField(max_length=100)),
                ('father_qualification', models.CharField(max_length=100)),
                ('father_profession', models.CharField(max_length=100)),
                ('father_designation', models.CharField(max_length=100)),
                ('father_aadhar_card', models.CharField(default='0', max_length=12)),
                ('father_mobile_number', models.CharField(max_length=12)),
                ('father_email', models.EmailField(blank=True, max_length=70, null=True)),
                ('mother_name', models.CharField(max_length=100)),
                ('mother_qualification', models.CharField(max_length=100)),
                ('mother_profession', models.CharField(max_length=100)),
                ('mother_designation', models.CharField(max_length=100)),
                ('mother_aadhar_card', models.CharField(default='0', max_length=12)),
                ('mother_mobile_number', models.CharField(max_length=12)),
                ('mother_email', models.EmailField(blank=True, max_length=70, null=True)),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='testapi.student')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_file', models.FileField(upload_to='documents/')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapi.student')),
            ],
        ),
        migrations.CreateModel(
            name='Academic_Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=100)),
                ('section', models.CharField(max_length=100)),
                ('date_of_joining', models.DateField()),
                ('enrollment_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapi.student')),
            ],
        ),
    ]
