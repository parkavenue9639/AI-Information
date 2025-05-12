from django.db import models

# Create your models here.

class NewsFlash(models.Model):
    REGION_CHOICES = (
        ('国内', '国内'),
        ('国外', '国外'),
    )
    date = models.DateField()
    region = models.CharField(max_length=10, choices=REGION_CHOICES)
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=60)
    detail = models.TextField()
    image_url = models.CharField(max_length=255)
    source_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'news_flash'
        verbose_name = '简讯'
        verbose_name_plural = '简讯'
