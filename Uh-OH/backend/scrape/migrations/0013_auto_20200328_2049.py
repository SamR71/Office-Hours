# Generated by Django 3.0.3 on 2020-03-29 00:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0012_merge_20200328_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='currentCourse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instructors', to='scrape.Course'),
        ),
        migrations.AlterField(
            model_name='instructorofficehours',
            name='meetInstructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='iOfficeHours', to='scrape.Instructor'),
        ),
    ]
