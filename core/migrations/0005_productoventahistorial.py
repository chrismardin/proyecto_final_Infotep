from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_movimientofinanciero_cliente_proveedor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductoVentaHistorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=20, unique=True, verbose_name='SKU/Cod')),
                ('nombre', models.CharField(max_length=120)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('actualizado', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['nombre'],
            },
        ),
    ]
