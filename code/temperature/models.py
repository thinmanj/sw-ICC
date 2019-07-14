from django.db import models
from modelchoices import Choices

from string import Template
import jsonpath_rw_ext as jp

import requests

import logging


logger = logging.getLogger("django")


class Services(models.Model):

    # As initial specifications only use GET and POST
    # Possible additions could be SOCKET or FILE, etc.
    class Methods(Choices):
        GET = ('get', 'GET')
        POST = ('post', 'POST')

    # Supporting functions for extensionability
    # use GET to collect information from source
    def get(self, latitude, longitude):
        query = Template(self.url_pattern).substitute(latitude=latitude, longitude=longitude)

        logger.info(f"get for {query}")

        return requests.get(query)

    # use POST to collect information
    def post(self, latitude, longitude):
        query = Template(self.url_pattern).substitute(latitude=latitude, longitude=longitude)
        if self.payload:
            payload = Template(self.payload).substitute(latitude=latitude, longitude=longitude)
        else:
            logger.info(f"No Payload on {self.name}")
            payload = None

        logger.info(f"post for {query}")

        return requests.post(query, data=payload,
                             headers={'Content-type': 'application/json', 'Accept': 'text/plain'})

    # Fields definitions
    name = models.CharField(max_length=80)
    url_pattern = models.CharField(max_length=2048) # comminity deffined
    payload = models.CharField(max_length=2048, blank=True)
    method = models.CharField(max_length=6, choices=Methods.CHOICES, default=Methods.GET)
    path = models.CharField(max_length=2048)
    enabled = models.BooleanField(default=False)

    # Entry points
    # Each entry know how to process its information
    def process(self, latitude, longitude):

        action = getattr(self, self.method)
        logger.info(f"Processing {self.name}: {self.method}")
        data = action(latitude, longitude)
        logger.info(f"Result: {data.status_code}")
        if data.status_code == requests.codes.ok:
            answer = float(jp.match1(self.path, data.json()))
            if not answer:
                raise ValueError("Didn't found a correct value or unknown answer")
                logger.error(f"{self.name} error no correct value found")
        return answer
