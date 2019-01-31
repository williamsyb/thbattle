# Generated by Django 2.1.2 on 2018-11-30 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('badge', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guild',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='名称', max_length=20, unique=True, verbose_name='名称')),
                ('slogan', models.CharField(help_text='口号', max_length=200, verbose_name='口号')),
                ('totem', models.ImageField(blank=True, help_text='图腾', upload_to='', verbose_name='图腾')),
                ('founded_at', models.DateTimeField(auto_now_add=True, help_text='创建日期', verbose_name='创建日期')),
                ('badges', models.ManyToManyField(help_text='勋章', related_name='guilds', to='badge.Badge', verbose_name='勋章')),
            ],
            options={
                'verbose_name': '势力',
                'verbose_name_plural': '势力',
            },
        ),
    ]