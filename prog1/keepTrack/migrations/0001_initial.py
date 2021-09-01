# Generated by Django 3.2.6 on 2021-09-01 12:31

import ckeditor.fields
import datetime
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('is_admin', models.BooleanField(default=False)),
                ('details', models.CharField(max_length=200)),
                ('banned', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['username'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_name', models.CharField(max_length=200)),
                ('start_date', models.DateTimeField(default=datetime.datetime.now)),
                ('due_date', models.DateTimeField()),
                ('is_completed', models.BooleanField(default=False)),
                ('description', models.TextField()),
            ],
            options={
                'ordering': ['due_date'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=200, unique=True)),
                ('start_date', models.DateTimeField(default=datetime.datetime.now)),
                ('due_date', models.DateTimeField()),
                ('wiki', ckeditor.fields.RichTextField()),
                ('is_completed', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='proj_creator', to=settings.AUTH_USER_MODEL)),
                ('members_p', models.ManyToManyField(related_name='members_p', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['due_date'],
            },
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_name', models.CharField(max_length=200)),
                ('start_date', models.DateTimeField(default=datetime.datetime.now)),
                ('due_date', models.DateTimeField()),
                ('is_completed', models.BooleanField(default=False)),
                ('members_l', models.ManyToManyField(related_name='members_l', to=settings.AUTH_USER_MODEL)),
                ('project_l', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keepTrack.project')),
                ('tags_l', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'ordering': ['due_date'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_content', models.TextField()),
                ('time', models.DateTimeField(default=datetime.datetime.now)),
                ('card', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='keepTrack.card')),
                ('list', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='keepTrack.list')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keepTrack.project')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comment_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['time'],
            },
        ),
        migrations.AddField(
            model_name='card',
            name='list_c',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keepTrack.list'),
        ),
        migrations.AddField(
            model_name='card',
            name='members_c',
            field=models.ManyToManyField(related_name='members_c', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='card',
            name='project_c',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keepTrack.project'),
        ),
        migrations.AddField(
            model_name='card',
            name='tags_c',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
