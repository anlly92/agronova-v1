# Generated by Django 5.2.2 on 2025-07-09 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventarios', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventario',
            name='id_tipo',
        ),
        migrations.AddField(
            model_name='inventario',
            name='tipo',
            field=models.CharField(default='Desconocido', max_length=50),
        ),
        migrations.DeleteModel(
            name='TipoInventario',
        ),
    ]
