# Generated by Django 2.1.2 on 2018-12-04 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokopedia', '0026_auto_20181203_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='good',
            name='last_scrapped',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]