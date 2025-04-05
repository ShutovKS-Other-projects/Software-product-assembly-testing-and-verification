# Generated by Django 5.1.7 on 2025-04-05 11:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormFactor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='Форм-фактор')),
            ],
        ),
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='Интерфейс')),
            ],
        ),
        migrations.AlterField(
            model_name='ssd',
            name='form_factor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.formfactor', verbose_name='Форм-фактор'),
        ),
        migrations.AlterField(
            model_name='ssd',
            name='interface',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.interface', verbose_name='Интерфейс'),
        ),
    ]
