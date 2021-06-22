# Generated by Django 3.1.3 on 2021-05-04 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0003_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=126, verbose_name='종목')),
                ('content', models.TextField(verbose_name='내용')),
                ('created_at', models.DateTimeField(verbose_name='작성일')),
            ],
        ),
    ]