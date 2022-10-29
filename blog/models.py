from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    html_content = models.TextField(blank=True, null=True)
    template_key = models.CharField(max_length=32)
    status = models.CharField(max_length=16)

    def __str__(self):
        return self.title
