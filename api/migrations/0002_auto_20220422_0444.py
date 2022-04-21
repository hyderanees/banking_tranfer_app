# Generated by Django 3.1.8 on 2022-04-21 23:44

import api.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='bank',
            table='Bank',
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_column='title', max_length=50)),
                ('IBAN', models.CharField(db_column='IBAN', default=api.utils.create_new_iban_number, editable=False, max_length=10, unique=True)),
                ('balance', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='updated_at')),
                ('bank', models.ForeignKey(db_column='bank', on_delete=django.db.models.deletion.CASCADE, to='api.bank')),
                ('owner', models.ForeignKey(db_column='owner', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Account',
            },
        ),
    ]