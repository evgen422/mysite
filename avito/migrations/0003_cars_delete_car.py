# Generated by Django 4.2 on 2023-04-23 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avito', '0002_alter_car_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cars',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('date', models.DateField(blank=True, null=True)),
                ('city', models.TextField(blank=True, null=True)),
                ('make', models.TextField(blank=True, null=True)),
                ('model', models.TextField(blank=True, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('mileage', models.IntegerField(blank=True, null=True)),
                ('power', models.IntegerField(blank=True, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('link', models.TextField(blank=True, null=True)),
                ('type', models.TextField(blank=True, null=True)),
                ('wd', models.TextField(blank=True, null=True)),
                ('fuel', models.TextField(blank=True, null=True)),
                ('comment_text', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'cars',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='Car',
        ),
    ]
