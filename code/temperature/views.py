from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from string import Template
import jsonpath_rw_ext as jp

import requests

from .models import Services

@api_view(['GET'])
def temperature(request, latitude, longitude):


    # Try to get the list of services the calls want to use
    services = set(Services.objects.values_list("name", flat=True).distinct())

    use = request.GET.get('use', False)
    if use:
        use = set(use.split(','))
        services = services & use

    if not services:
        return Response({"message": "No options selected"},
                        status=status.HTTP_400_BAD_REQUEST)

    # call each service on sequence and collect it result
    result = []
    for service in Services.objects.filter(name__in=services).all():
        s = Template(service.url_pattern)
        payload = Template(service.payload)

        action = getattr(requests, service.method)

        data = action(s.substitute(latitude=latitude, longitude=longitude),
                      data=payload.substitute(latitude=latitude, longitude=longitude),
                      headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
        if data.status_code == requests.codes.ok:
            answer = float(jp.match1(service.path, data.json()))
            if answer:
                result.append(answer)

    # If no result no service answered a correct json, bail out
    if not result:
        return Response({"message": "No enough data to be processed"},
                        status=status.HTTP_400_BAD_REQUEST)

    average = sum(result) / len(result)

    # returns a simple dictionary
    return Response({"average": average})
