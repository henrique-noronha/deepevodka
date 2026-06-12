from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('data', models.DateField()),
                ('hora', models.TimeField()),
                ('local', models.CharField(max_length=200)),
                ('banner', models.ImageField(blank=True, null=True, upload_to='eventos/banners/')),
                ('descricao', models.TextField(blank=True)),
                ('capacidade', models.IntegerField(blank=True, null=True)),
                ('link_ingresso', models.URLField(blank=True, null=True)),
            ],
            options={
                'ordering': ['data', 'hora'],
            },
        ),
    ]
