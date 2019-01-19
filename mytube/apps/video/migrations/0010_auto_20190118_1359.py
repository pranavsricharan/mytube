# Generated by Django 2.1.3 on 2019-01-18 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('video', '0009_history'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(choices=[('LIKE', 'Like'), ('UNLIKE', 'Unlike')], default='LIKE', max_length=6)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='video.Video')),
            ],
        ),
        migrations.AlterModelOptions(
            name='history',
            options={'ordering': ['-watched_time'], 'verbose_name_plural': 'history entries'},
        ),
    ]