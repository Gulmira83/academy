# Generated by Django 3.0.3 on 2020-05-25 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20200525_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='feature_type',
            field=models.CharField(default='Basic', max_length=60),
        ),
    ]
