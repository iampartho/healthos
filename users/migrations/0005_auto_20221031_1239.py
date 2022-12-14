# Generated by Django 3.2 on 2022-10-31 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.company'),
        ),
        migrations.AlterField(
            model_name='user',
            name='plan',
            field=models.CharField(blank=True, choices=[('Bronze', 'Globalnet Bronze - 500 BDT // month, 12 months'), ('Silver', 'Globalnet Silver - 750 BDT / month, 12 months'), ('Gold', 'Globalnet Gold - 1500 BDT / month, no contract - You can cancel at any time')], max_length=200, null=True),
        ),
    ]
