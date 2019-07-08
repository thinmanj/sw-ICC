from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('temperature', '0001_initial'), ('temperature', '0002_auto_20190708_0206'), ('temperature', '0003_services_method'), ('temperature', '0004_auto_20190708_0350'), ('temperature', '0005_auto_20190708_0419')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('url_pattern', models.CharField(max_length=2048)),
                ('enabled', models.BooleanField(default=False)),
                ('method', models.CharField(choices=[('get', 'GET'), ('post', 'POST')], default='get', max_length=6)),
                ('path', models.CharField(default=' ', max_length=2048)),
                ('payload', models.CharField(blank=True, max_length=2048)),
            ],
        ),
    ]
