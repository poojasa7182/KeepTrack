# Generated by Django 3.2.6 on 2021-09-06 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keepTrack', '0010_alter_list_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='card',
            unique_together={('list_c', 'card_name')},
        ),
    ]
