# Generated by Django 3.2.9 on 2021-12-28 21:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('gender', models.CharField(choices=[('female', 'female'), ('male', 'male')], max_length=6)),
                ('date_of_birth', models.DateField()),
                ('father', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children_dad', to='personapp.person')),
                ('mother', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children_mom', to='personapp.person')),
            ],
        ),
    ]