# Generated by Django 5.1.6 on 2025-05-05 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0029_alter_work_finish'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='work',
            name='category',
        ),
        migrations.AlterField(
            model_name='education',
            name='type',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='work',
            name='type',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
