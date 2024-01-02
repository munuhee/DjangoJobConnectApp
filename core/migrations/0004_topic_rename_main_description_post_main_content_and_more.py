# Generated by Django 4.2.6 on 2024-01-01 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_post_subscription_required'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a Topic name', max_length=50)),
            ],
        ),
        migrations.RenameField(
            model_name='post',
            old_name='main_description',
            new_name='main_content',
        ),
        migrations.RemoveField(
            model_name='post',
            name='categories',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.AddField(
            model_name='post',
            name='topics',
            field=models.ManyToManyField(help_text='Select categories for this post', to='core.topic'),
        ),
    ]