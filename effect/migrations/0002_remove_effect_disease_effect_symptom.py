# Generated by Django 4.2.9 on 2024-02-10 04:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('symptom', '0003_rename_value_symptom_name'),
        ('effect', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='effect',
            name='disease',
        ),
        migrations.AddField(
            model_name='effect',
            name='symptom',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='symptom.symptom'),
            preserve_default=False,
        ),
    ]