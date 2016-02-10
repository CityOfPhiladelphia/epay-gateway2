# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-09 21:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('slug', models.CharField(max_length=64)),
                ('price', models.PositiveIntegerField(null=True)),
                ('summary', models.TextField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(to='epay.ProductCategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='department',
            field=models.ManyToManyField(to='epay.Department'),
        ),
    ]