# Generated by Django 3.2.9 on 2021-12-17 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_tool', '0003_auto_20211217_0210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systems',
            name='debBootIndex',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='systems',
            name='ubuBootIndex',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='systems',
            name='winBootIndex',
            field=models.IntegerField(null=True),
        ),
    ]
