# Generated by Django 5.0.6 on 2024-06-18 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packs', '0025_alter_subscription_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='name',
            field=models.CharField(default='hjhjhjhjh', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pack',
            name='amount_per_month',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
