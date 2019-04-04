from django.conf import settings
from django.db import models
from django.urls import reverse
import django_filters
from .classifier import classify_defect

STATUS_CHOICES_SOURCE = (
    ('csv', 'csv'),
    ('Entry', 'Entry'),
)

STATUS_CHOICES_CLASS = (
    ('Compliance', 'Compliance'),
    ('Functional', 'Functional'),
    ('Performance', 'Performance'),
    ('Reliability and Scalability', 'Reliability and Scalability'),
    ('Security', 'Security'),
    ('Usability', 'Usability'),
)

classes = (
    ('Compliance', 'COMPLIANCE'),
    ('Functional', 'FUNCTIONAL'),
    ('Performance', 'PERFORMANCE'),
    ('Reliability and scalability', 'RELIABILITY AND SCALABILITY'),
    ('Security', 'SECURITY'),
    ('Usability', 'USABILITY'),
)

class Article(models.Model):
    body = models.TextField()
    source = models.CharField(default='Entry', max_length=20, choices=STATUS_CHOICES_SOURCE)
    date = models.DateTimeField(auto_now_add=True)
    classification = models.CharField(default = 'Not Classified', max_length = 40, choices=STATUS_CHOICES_CLASS)
    reclassification = models.CharField(default = 'Not Classified Yet', max_length = 40, choices = classes)


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
