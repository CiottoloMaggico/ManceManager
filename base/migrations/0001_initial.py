# Generated by Django 4.2.5 on 2023-09-19 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveBigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Quarter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quarters', to='base.year')),
            ],
        ),
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('quarter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='months', to='base.quarter')),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_hour', models.TimeField()),
                ('end_hour', models.TimeField()),
                ('note', models.TextField(blank=True, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activities', to='base.category')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', related_query_name='activity', to='base.client')),
            ],
        ),
        migrations.CreateModel(
            name='Parcel',
            fields=[
                ('year_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='base.year')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parcels', related_query_name='parcel', to='base.client')),
            ],
            bases=('base.year',),
        ),
    ]
