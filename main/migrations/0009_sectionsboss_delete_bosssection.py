# Generated by Django 4.2.5 on 2024-04-28 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_country_shopcategory_socialnetworksboss_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SectionsBoss',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='image/boss_section/%Y-%m-%d/', verbose_name='Rasmi')),
                ('f_name', models.CharField(max_length=150, verbose_name="To'liq ismi")),
                ('f_name_uz', models.CharField(max_length=150, null=True, verbose_name="To'liq ismi")),
                ('f_name_ru', models.CharField(max_length=150, null=True, verbose_name="To'liq ismi")),
                ('f_name_en', models.CharField(max_length=150, null=True, verbose_name="To'liq ismi")),
                ('email', models.CharField(max_length=250, verbose_name='Email')),
                ('phone', models.CharField(max_length=250, verbose_name='Telefon raqami')),
                ('position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.positions', verbose_name='Lavozimi')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sections_boss', to='main.posts', verbose_name='post')),
            ],
            options={
                'verbose_name': "Bo'lim raxbarlari",
                'db_table': 'sections_bosses',
                'ordering': ['position'],
            },
        ),
        migrations.DeleteModel(
            name='BossSection',
        ),
    ]
