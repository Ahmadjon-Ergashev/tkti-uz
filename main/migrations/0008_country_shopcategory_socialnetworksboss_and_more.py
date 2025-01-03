# Generated by Django 4.2.5 on 2024-04-23 15:45

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_aboutstudyprogrampdf_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nomi')),
                ('name_uz', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nomi')),
                ('name_ru', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nomi')),
                ('name_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nomi')),
                ('order_num', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Davlatlar',
                'verbose_name_plural': 'Davlatlar',
                'db_table': 'country',
                'ordering': ('order_num',),
            },
        ),
        migrations.CreateModel(
            name='ShopCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nomi')),
                ('name_uz', models.CharField(max_length=255, null=True, verbose_name='Nomi')),
                ('name_ru', models.CharField(max_length=255, null=True, verbose_name='Nomi')),
                ('name_en', models.CharField(max_length=255, null=True, verbose_name='Nomi')),
            ],
            options={
                'verbose_name': "Shop Bo'limlari",
                'verbose_name_plural': "Shop Bo'limlari",
                'db_table': 'shop_category',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='SocialNetworksBoss',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nomi')),
                ('icon', models.CharField(blank=True, max_length=255, null=True, verbose_name='Icon')),
                ('color', colorfield.fields.ColorField(blank=True, default='#123456', image_field=None, max_length=25, null=True, samples=None, verbose_name='rangi')),
            ],
            options={
                'verbose_name': 'Ijtimoiy tarmoqlar Xodimlar',
                'verbose_name_plural': 'Ijtimoiy tarmoqlar Xodimlar',
                'db_table': 'social_networks_boss',
            },
        ),
        migrations.AlterModelOptions(
            name='entryrequirements',
            options={'ordering': ('-id',), 'verbose_name': 'Kirish talablari', 'verbose_name_plural': 'Kirish talablari'},
        ),
        migrations.AddField(
            model_name='news',
            name='author_post_en',
            field=models.CharField(default='TKTI axborot xizmati', max_length=300, null=True, verbose_name='Muallifi'),
        ),
        migrations.AddField(
            model_name='news',
            name='author_post_ru',
            field=models.CharField(default='TKTI axborot xizmati', max_length=300, null=True, verbose_name='Muallifi'),
        ),
        migrations.AddField(
            model_name='news',
            name='author_post_uz',
            field=models.CharField(default='TKTI axborot xizmati', max_length=300, null=True, verbose_name='Muallifi'),
        ),
        migrations.AddField(
            model_name='posts',
            name='author_post_en',
            field=models.CharField(default='TKTI axborot xizmati', max_length=300, null=True, verbose_name='Muallifi'),
        ),
        migrations.AddField(
            model_name='posts',
            name='author_post_ru',
            field=models.CharField(default='TKTI axborot xizmati', max_length=300, null=True, verbose_name='Muallifi'),
        ),
        migrations.AddField(
            model_name='posts',
            name='author_post_uz',
            field=models.CharField(default='TKTI axborot xizmati', max_length=300, null=True, verbose_name='Muallifi'),
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nomi')),
                ('name_uz', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nomi')),
                ('name_ru', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nomi')),
                ('name_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nomi')),
                ('image', models.ImageField(blank=True, null=True, upload_to='tkti_shop_images/')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('contact', models.CharField(blank=True, max_length=255, null=True, verbose_name="Ma'sul shaxs")),
                ('phone_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Telefon raqam')),
                ('telegram', models.CharField(blank=True, max_length=100, null=True, verbose_name='Telegram manzil')),
                ('instagram', models.CharField(blank=True, max_length=100, null=True, verbose_name='Instagram link')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.shopcategory')),
            ],
            options={
                'verbose_name': 'TKTI Shop',
                'verbose_name_plural': 'TKTI Shop',
                'db_table': 'shop',
                'ordering': ('-added_at',),
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nomi')),
                ('name_uz', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nomi')),
                ('name_ru', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nomi')),
                ('name_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nomi')),
                ('image', models.ImageField(blank=True, null=True, upload_to='partners/')),
                ('url', models.URLField(blank=True, max_length=400, null=True, verbose_name='URL manzil')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='partners_country', to='main.country', verbose_name='Davlat')),
            ],
            options={
                'verbose_name': 'Hamkorlar',
                'verbose_name_plural': 'Hamkorlar',
                'db_table': 'partners',
                'ordering': ('country',),
            },
        ),
        migrations.CreateModel(
            name='NetworksBoss',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(blank=True, max_length=255, null=True, verbose_name='URL')),
                ('boss', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='boss_network', to='main.universityadmistrations')),
                ('social_networks', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.socialnetworksboss')),
            ],
            options={
                'verbose_name': 'Rahbariat ijtimoiy tarmoqlar',
                'verbose_name_plural': 'Rahbariat ijtimoiy tarmoqlar',
                'db_table': 'networks_boss',
            },
        ),
    ]
