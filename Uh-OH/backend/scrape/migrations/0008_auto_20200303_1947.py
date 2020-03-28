# Generated by Django 3.0.3 on 2020-03-04 00:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0007_auto_20200220_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursemeetingtime',
            name='meetSection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courseMeetingTimes', to='scrape.CourseSection'),
        ),
        migrations.AlterField(
            model_name='coursesection',
            name='currentCourse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='scrape.Course'),
        ),
    ]