# Generated by Django 3.2.9 on 2021-12-17 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_tool', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='processtracker',
            name='procId',
        ),
        migrations.RemoveField(
            model_name='processtracker',
            name='userEmail',
        ),
        migrations.AddField(
            model_name='processtracker',
            name='id',
            field=models.BigAutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='processtracker',
            name='modsRunningStatus',
            field=models.CharField(default='f', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='processtracker',
            name='procIDs',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='processtracker',
            name='systemIDs',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='processtracker',
            name='testCompletionStatus',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='processtracker',
            name='userProcNum',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='processtracker',
            name='username',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='systems',
            name='currentOS',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
