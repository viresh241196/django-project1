# Generated by Django 3.1 on 2020-08-26 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_blog', '0003_auto_20200826_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='post_img'),
        ),
    ]
