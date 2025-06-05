from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('khschool', '0005_alter_celebration_image_celebrationphoto'),
    ]

    operations = [
        # Add image_url field to Celebration model
        migrations.AddField(
            model_name='celebration',
            name='image_url',
            field=models.CharField(blank=True, max_length=500, verbose_name='Main Image (Supabase)'),
        ),
        
        # Add photo_url field to CelebrationPhoto model
        migrations.AddField(
            model_name='celebrationphoto',
            name='photo_url',
            field=models.CharField(blank=True, max_length=500, verbose_name='Photo (Supabase)'),
        ),
        
        # Add image_url field to CarouselImage model
        migrations.AddField(
            model_name='carouselimage',
            name='image_url',
            field=models.CharField(blank=True, max_length=500, verbose_name='Image (Supabase)'),
        ),
        
        # Make original image fields optional
        migrations.AlterField(
            model_name='celebration',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='festival/images/', verbose_name='Main Image'),
        ),
        
        migrations.AlterField(
            model_name='celebrationphoto',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='festival/gallery/', verbose_name='Photo'),
        ),
        
        migrations.AlterField(
            model_name='carouselimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='carousel/images/'),
        ),
    ]
