# Generated by Django 4.2.5 on 2024-03-13 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_semesters_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseVariables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='image/logos/')),
                ('name', models.CharField(blank=True, max_length=125, null=True, verbose_name='Nomi')),
                ('name_uz', models.CharField(blank=True, max_length=125, null=True, verbose_name='Nomi')),
                ('name_ru', models.CharField(blank=True, max_length=125, null=True, verbose_name='Nomi')),
                ('name_en', models.CharField(blank=True, max_length=125, null=True, verbose_name='Nomi')),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=125, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('description_uz', models.TextField(blank=True, null=True)),
                ('description_ru', models.TextField(blank=True, null=True)),
                ('description_en', models.TextField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('address_uz', models.TextField(blank=True, null=True)),
                ('address_ru', models.TextField(blank=True, null=True)),
                ('address_en', models.TextField(blank=True, null=True)),
                ('buses', models.CharField(blank=True, max_length=125, null=True)),
                ('buses_uz', models.CharField(blank=True, max_length=125, null=True)),
                ('buses_ru', models.CharField(blank=True, max_length=125, null=True)),
                ('buses_en', models.CharField(blank=True, max_length=125, null=True)),
            ],
            options={
                'verbose_name': "Asosiy o'zgaruvchilar",
                'verbose_name_plural': "Asosiy o'zgaruvchilar",
                'db_table': 'base_variables',
            },
        ),
        migrations.CreateModel(
            name='Positions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('name_uz', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('name_ru', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('name_en', models.CharField(blank=True, max_length=255, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'Lavozimlar',
                'verbose_name_plural': 'Lavozimlar',
                'db_table': 'positions',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='TopNavbar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nomi')),
                ('name_uz', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nomi')),
                ('name_ru', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nomi')),
                ('name_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nomi')),
                ('url', models.URLField(blank=True, max_length=500, null=True)),
                ('order_num', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Top Navbar',
                'verbose_name_plural': 'Top Navbar',
                'db_table': 'top_navbar',
                'ordering': ('order_num',),
            },
        ),
        migrations.AddField(
            model_name='extrafile',
            name='brm_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='brm_extra_file', to='main.brmitems'),
        ),
        migrations.AddField(
            model_name='sectionsandcenters',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image/sections_and_centers/'),
        ),
        migrations.AlterField(
            model_name='ads',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image/%Y-%m-%d/', verbose_name='Asosiy rasm'),
        ),
        migrations.AlterField(
            model_name='events',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image/%Y-%m-%d/', verbose_name='Asosiy rasm'),
        ),
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image/%Y-%m-%d/', verbose_name='Asosiy rasm'),
        ),
        migrations.AlterField(
            model_name='posts',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image/%Y-%m-%d/', verbose_name='Asosiy rasm'),
        ),
        migrations.AddField(
            model_name='bosssection',
            name='self_position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.positions', verbose_name='Lavozimi'),
        ),
        migrations.AddField(
            model_name='workers',
            name='self_position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.positions', verbose_name='Lavozimi'),
        ),
    ]