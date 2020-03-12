# Generated by Django 3.0.3 on 2020-03-10 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hbpapp', '0002_auto_20200108_1822'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docfile', models.FileField(upload_to='documents/%Y/%m/%d')),
            ],
        ),
        migrations.AlterModelOptions(
            name='transactions',
            options={'ordering': ['tr_date', 'tr_time', 'Sum', 'CCY']},
        ),
    ]
