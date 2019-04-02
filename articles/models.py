from django.conf import settings
from django.db import models
from django.urls import reverse


from .classifier import classify_defect

class Article(models.Model):
    body = models.TextField()
    source = models.CharField(default='Entry', max_length=20)
    date = models.DateTimeField(auto_now_add=True)
    classification = models.CharField(default = 'Not Classified', max_length = 20)

    def __str__(self):
        return self.body

    def body_str(self):
        new_text = classify_defect(self.body)
        return new_text

    def get_absolute_url(self):
        return reverse('table')

    def save(self, *args, **kwargs):
        self.classification = self.body_str()
        super().save(*args, **kwargs)
