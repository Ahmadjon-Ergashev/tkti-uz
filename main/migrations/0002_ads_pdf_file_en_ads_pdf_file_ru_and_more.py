# Generated by Django 4.2.5 on 2024-02-22 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ads',
            name='pdf_file_en',
            field=models.FileField(blank=True, help_text='Faqat *.pdf formatdagi faylarni yuklang', null=True, upload_to='pdf/en/ads/%Y-%m-%d/', verbose_name='EN PDF fayl'),
        ),
        migrations.AddField(
            model_name='ads',
            name='pdf_file_ru',
            field=models.FileField(blank=True, help_text='Faqat *.pdf formatdagi faylarni yuklang', null=True, upload_to='pdf/ru/ads/%Y-%m-%d/', verbose_name='RU PDF fayl'),
        ),
        migrations.AddField(
            model_name='departments',
            name='pdf_file_en',
            field=models.FileField(blank=True, help_text='Faqat PDF formatidagi faylni joylang', null=True, upload_to='pdf/en/departments/%Y-%m-%d/', verbose_name='EN PDF fayl'),
        ),
        migrations.AddField(
            model_name='departments',
            name='pdf_file_ru',
            field=models.FileField(blank=True, help_text='Faqat PDF formatidagi faylni joylang', null=True, upload_to='pdf/ru/departments/%Y-%m-%d/', verbose_name='RU PDF fayl'),
        ),
        migrations.AddField(
            model_name='educationalareas',
            name='pdf_file_en',
            field=models.FileField(blank=True, help_text='Faqat *.pdf formatdagi faylarni yuklang', max_length=255, null=True, upload_to='pdf/en/educational_areas/%Y-%m-%d/', verbose_name='EN PDF fayl'),
        ),
        migrations.AddField(
            model_name='educationalareas',
            name='pdf_file_ru',
            field=models.FileField(blank=True, help_text='Faqat *.pdf formatdagi faylarni yuklang', max_length=255, null=True, upload_to='pdf/ru/educational_areas/%Y-%m-%d/', verbose_name='RU PDF fayl'),
        ),
        migrations.AddField(
            model_name='events',
            name='pdf_file_en',
            field=models.FileField(blank=True, help_text='Faqat *.pdf formatdagi faylarni yuklang', null=True, upload_to='pdf/en/news/%Y-%m-%d/', verbose_name='EN PDF fayl'),
        ),
        migrations.AddField(
            model_name='events',
            name='pdf_file_ru',
            field=models.FileField(blank=True, help_text='Faqat *.pdf formatdagi faylarni yuklang', null=True, upload_to='pdf/ru/news/%Y-%m-%d/', verbose_name='RU PDF fayl'),
        ),
        migrations.AddField(
            model_name='extrafile',
            name='pdf_file_en',
            field=models.FileField(blank=True, null=True, upload_to='pdf/en/extra_files/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='extrafile',
            name='pdf_file_ru',
            field=models.FileField(blank=True, null=True, upload_to='pdf/ru/extra_files/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='moduleofstudyprograme',
            name='pdf_file_en',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to='pdf/en/modules_of_study_programe/%Y-%m-%d/', verbose_name='EN PDF fayl'),
        ),
        migrations.AddField(
            model_name='moduleofstudyprograme',
            name='pdf_file_ru',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to='pdf/ru/modules_of_study_programe/%Y-%m-%d/', verbose_name='RU PDF fayl'),
        ),
        migrations.AddField(
            model_name='navbar',
            name='url',
            field=models.URLField(blank=True, help_text='Tegish shart emas', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='news',
            name='pdf_file_en',
            field=models.FileField(blank=True, help_text='Faqat *.pdf formatdagi faylarni yuklang', null=True, upload_to='pdf/en/news/%Y-%m-%d/', verbose_name='EN PDF fayl'),
        ),
        migrations.AddField(
            model_name='news',
            name='pdf_file_ru',
            field=models.FileField(blank=True, help_text='Faqat *.pdf formatdagi faylarni yuklang', null=True, upload_to='pdf/ru/news/%Y-%m-%d/', verbose_name='RU PDF fayl'),
        ),
        migrations.AddField(
            model_name='posts',
            name='pdf_file_en',
            field=models.FileField(blank=True, help_text='Faqat *.pdf formatdagi faylarni yuklang', null=True, upload_to='pdf/en/posts/%Y-%m-%d/', verbose_name='EN PDF file'),
        ),
        migrations.AddField(
            model_name='posts',
            name='pdf_file_ru',
            field=models.FileField(blank=True, help_text='Faqat *.pdf formatdagi faylarni yuklang', null=True, upload_to='pdf/ru/posts/%Y-%m-%d/', verbose_name='RU PDF file'),
        ),
        migrations.AddField(
            model_name='studyprogram',
            name='pdf_file_en',
            field=models.FileField(blank=True, null=True, upload_to='pdf/en/study_program/%Y-%m-%d/', verbose_name='EN PDF fayl'),
        ),
        migrations.AddField(
            model_name='studyprogram',
            name='pdf_file_ru',
            field=models.FileField(blank=True, null=True, upload_to='pdf/ru/study_program/%Y-%m-%d/', verbose_name='RU PDF fayl'),
        ),
        migrations.AlterField(
            model_name='studyprogram',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='pdf/study_program/%Y-%m-%d/', verbose_name='PDF fayl'),
        ),
    ]