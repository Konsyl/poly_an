# Generated by Django 3.1 on 2020-09-03 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polygon_rest', '0005_auto_20200903_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dot',
            name='frectangle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dots', to='polygon_rest.frectangle'),
        ),
    ]