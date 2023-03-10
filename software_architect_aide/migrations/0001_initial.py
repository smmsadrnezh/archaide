# Generated by Django 2.2 on 2020-07-22 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Architecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('owl_file', models.FileField(upload_to='media/owl')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='architectures', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
