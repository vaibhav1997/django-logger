# Generated by Django 2.1.7 on 2019-05-21 06:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userlog', '0006_auto_20190521_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logger',
            name='user',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
