# Generated by Django 4.2.5 on 2024-09-29 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_remove_universityadmistrations_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepartmentPlanDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_plan', models.FileField(blank=True, null=True, upload_to='pdf/department_files/plan/uz/%Y-%m-%d/', verbose_name='Kafedra rejasi')),
                ('department_plan_en', models.FileField(blank=True, null=True, upload_to='pdf/department_files/plan/en/%Y-%m-%d/', verbose_name='Department plan')),
                ('department_plan_ru', models.FileField(blank=True, null=True, upload_to='pdf/department_files/plan/ru/%Y-%m-%d/', verbose_name='План отдела')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='department_plan_files', to='main.departments')),
            ],
            options={
                'verbose_name': 'Kafedra rejasi',
                'verbose_name_plural': 'Kafedra rejasi',
                'db_table': 'department_plan_files_table',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DepartmentCharterDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_charter', models.FileField(blank=True, null=True, upload_to='pdf/department_files/charter/uz/%Y-%m-%d/', verbose_name='Kafedra nizomi')),
                ('department_charter_en', models.FileField(blank=True, null=True, upload_to='pdf/department_files/charter/en/%Y-%m-%d/', verbose_name='Department Charter')),
                ('department_charter_ru', models.FileField(blank=True, null=True, upload_to='pdf/department_files/charter/ru/%Y-%m-%d/', verbose_name='Устав кафедры')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='department_charter_files', to='main.departments')),
            ],
            options={
                'verbose_name': 'Kafedra nizomi',
                'verbose_name_plural': 'Kafedra nizomi',
                'db_table': 'department_charter_files_table',
                'managed': True,
            },
        ),
    ]
