# Generated by Django 3.2 on 2021-05-05 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.IntegerField()),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=255)),
                ('level', models.IntegerField()),
                ('heat', models.IntegerField()),
                ('image', models.CharField(max_length=255, null=True)),
                ('category', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Mate',
            fields=[
                ('mate_id', models.AutoField(primary_key=True, serialize=False)),
                ('establish_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('openid', models.CharField(max_length=255, unique=True)),
                ('username', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('resource_id', models.AutoField(primary_key=True, serialize=False)),
                ('resource_key', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=255)),
                ('content_type', models.IntegerField()),
                ('content', models.TextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inscourse_backend.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inscourse_backend.user')),
            ],
        ),
        migrations.CreateModel(
            name='MateAssignment',
            fields=[
                ('assignment_id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('status', models.IntegerField(default=0)),
                ('schedule_date', models.DateField()),
                ('done_date', models.DateField(default=None, null=True)),
                ('mate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inscourse_backend.mate')),
            ],
        ),
        migrations.CreateModel(
            name='MateInvitation',
            fields=[
                ('invitation_id', models.AutoField(primary_key=True, serialize=False)),
                ('request_time', models.DateTimeField()),
                ('status', models.IntegerField()),
                ('acceptor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accept_user', to='inscourse_backend.user')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inscourse_backend.course')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_user', to='inscourse_backend.user')),
            ],
        ),
        migrations.AddField(
            model_name='mate',
            name='acceptor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acceptor', to='inscourse_backend.user'),
        ),
        migrations.AddField(
            model_name='mate',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inscourse_backend.course'),
        ),
        migrations.AddField(
            model_name='mate',
            name='requester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requester', to='inscourse_backend.user'),
        ),
        migrations.CreateModel(
            name='CourseJoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inscourse_backend.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inscourse_backend.user')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inscourse_backend.user'),
        ),
    ]
