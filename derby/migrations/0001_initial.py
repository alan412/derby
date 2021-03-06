# Generated by Django 3.1.5 on 2021-02-07 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('picture', models.ImageField(upload_to='')),
                ('owner', models.CharField(max_length=200)),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Heat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('finished', models.BooleanField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='derby.group')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lane', models.IntegerField()),
                ('time', models.DurationField(null=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='derby.car')),
                ('heat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='derby.heat')),
            ],
        ),
        migrations.AddField(
            model_name='car',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='derby.group'),
        ),
        migrations.AddConstraint(
            model_name='heat',
            constraint=models.UniqueConstraint(fields=('group', 'number'), name='Unique heat number in group'),
        ),
        migrations.AddConstraint(
            model_name='car',
            constraint=models.UniqueConstraint(fields=('group', 'number'), name='Unique car number in group'),
        ),
    ]
