# Generated by Django 4.2.5 on 2024-02-28 02:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_brmitems_pdf_file_brmitems_pdf_file_en_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='semesters',
            options={'managed': True, 'ordering': ('name',), 'verbose_name': 'Semesterlar', 'verbose_name_plural': 'Semesterlar'},
        ),
    ]
