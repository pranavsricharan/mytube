# Generated by Django 2.1.3 on 2019-01-18 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0010_auto_20190118_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videorating',
            name='rating',
            field=models.CharField(choices=[('LIKE', 'Like'), ('DISLIKE', 'Dislike')], default='LIKE', max_length=7),
        ),
    ]
