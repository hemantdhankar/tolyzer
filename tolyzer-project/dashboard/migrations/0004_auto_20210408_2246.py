# Generated by Django 3.1.7 on 2021-04-08 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='submission_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
