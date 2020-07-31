# Generated by Django 2.2 on 2020-07-31 06:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('software_architect_aide', '0006_architecture_creation_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='architecture',
            name='parent_architecture',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='software_architect_aide.Architecture'),
        ),
        migrations.AlterField(
            model_name='architecture',
            name='creation_method',
            field=models.CharField(choices=[('manual', 'ساخت دستی'), ('reference', 'براساس معماری مرجع'), ('evolution', 'تکامل معماری'), ('upload', 'بارگذاری هستان\u200cشناسی')], max_length=30),
        ),
    ]