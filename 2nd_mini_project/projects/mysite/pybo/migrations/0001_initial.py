# Generated by Django 3.1.3 on 2021-05-03 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=126, verbose_name='종목')),
                ('content', models.TextField(verbose_name='매매종류')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='작성일')),
            ],
        ),
    ]
