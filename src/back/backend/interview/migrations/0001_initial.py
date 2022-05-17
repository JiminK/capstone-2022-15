# Generated by Django 4.0.3 on 2022-05-17 03:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interview_id', models.IntegerField(help_text='인터뷰 번호')),
                ('question_id', models.CharField(help_text='질문 번호', max_length=2)),
                ('interview_time', models.DateTimeField(auto_now_add=True, help_text='인터뷰 날짜')),
                ('field_id', models.IntegerField(help_text='분야')),
                ('interviewee_url', models.URLField(help_text='면접자 영상 저장 url')),
                ('author', models.ForeignKey(help_text='유저 정보', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
