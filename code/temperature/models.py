from django.db import models
from modelchoices import Choices


class Services(models.Model):

    class Methods(Choices):
        GET = ('get', 'GET')
        POST = ('post', 'POST')

    name = models.CharField(max_length=80)
    url_pattern = models.CharField(max_length=2048) # comminity deffined
    payload = models.CharField(max_length=2048, blank=True)
    method = models.CharField(max_length=6, choices=Methods.CHOICES, default=Methods.GET)
    path = models.CharField(max_length=2048)
    enabled = models.BooleanField(default=False)
