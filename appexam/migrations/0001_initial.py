# Generated by Django 4.2.4 on 2023-08-17 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bloguser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=250)),
                ('password', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Blogpost',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=250)),
                ('content', models.CharField(max_length=250)),
                ('created_at', models.BigIntegerField()),
                ('Blogcreator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appexam.bloguser')),
            ],
        ),
    ]