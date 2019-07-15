from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings

from statistics import mean, StatisticsError

from .models import Services
import logging
import requests

logger = logging.getLogger("django")


def validate(latitude, longitude):
    # simple range validation for latitude and longitude
    # no need for google maps on this
    # TODO: move to validators.py
    lat_ok = -180.0 <= float(latitude) <= 180.0
    lon_ok = -90.0 <= float(longitude) <= 90.0

    return lat_ok and lon_ok


def _filtering(request):
    # Try to get the list of services the call wants to use
    # TODO: move to filters.py
    services = set(Services.objects.values_list("name", flat=True).distinct())

    use = request.GET.get('use', False)
    if use:
        use = set(use.split(','))
        services = services & use # yeah simple intersection, to keep things flat

    if not services:
        logger.warning("no valid option on {use}")
        return Response({"message": "No enough options selected"},
                        status=status.HTTP_400_BAD_REQUEST)

    return services


@api_view(['GET'])
def geo_location(request, latitude, longitude):
    if not validate(latitude, longitude):
        logger.error(f"out of range lat:{latitude} lon:{longitude}")
        return Response(status=status.HTTP_404_NOT_FOUND)

    services = _filtering(request)

    return temperature(latitude, longitude, services)


@api_view(['GET'])
def zipcode(request, zipcode):
    if not settings.GOOGLE_MAPS_API_KEY:
        logger.error("No google maps api key defined")
        return Response({"message": "Missing configuration"},
                         status=status.HTTP_503_SERVICE_UNAVAILABLE)

    services = _filtering(request)

    api_response = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={zipcode}&key={settings.GOOGLE_MAPS_API_KEY}')

    if api_response.status_code == requests.codes.ok:
        api_response_dict = api_response.json()
        print(api_response_dict)
        try:
            latitude = api_response_dict['results'][0]['geometry']['location']['lat']
            longitude = api_response_dict['results'][0]['geometry']['location']['lng']
        except IndexError:
            logger.warning("Check Google limits")
            return Response({"message": "Bad asnwer, check service limits"},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return temperature(latitude, longitude, services)

    logger.warning("Couldn't process request")
    return Response({"message": "bad answer o no answer from service"},
                         status=status.HTTP_503_SERVICE_UNAVAILABLE)


def temperature(latitude, longitude, services):
    # call each service on sequence and collect its result
    # TODO: move to services.py
    result = []
    for service in Services.objects.filter(name__in=services).filter(enabled=True).all():
        try:
            answer = service.process(latitude, longitude)
            result.append(answer)
        except ValueError:
            # for this excercise, just ignore bad values
            logger.warning(f"exception from {service.name} calculation")
            pass

    try:
        average = mean(result)
    except StatisticsError:
        # no data, bail out
        logger.warning(f"could not generate a current answer")
        return Response({"message": "No enough data to be processed"},
                        status=status.HTTP_400_BAD_REQUEST)

    # returns a simple dictionary
    return Response({"average": average})
