# Generated by Django 4.1.5 on 2023-10-05 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0007_category_requirement_rename_title_job_company_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='company_description',
        ),
        migrations.RemoveField(
            model_name='job',
            name='location',
        ),
        migrations.RemoveField(
            model_name='job',
            name='requirements',
        ),
        migrations.RemoveField(
            model_name='job',
            name='thumbnail',
        ),
    ]