from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from statistics import mean, StatisticsError

from .models import Services
import logging


logger = logging.getLogger(__name__)


def validate(latitude, longitude):
    # simple range validation for latitude and longitude
    # no need for google maps on this
    lat_ok = -180.0 <= float(latitude) <= 180.0
    lon_ok = -90.0 <= float(longitude) <= 90.0

    return lat_ok and lon_ok


@api_view(['GET'])
def temperature(request, latitude, longitude):
    if not validate(latitude, longitude):
        logger.warning(f"out of range lat:{latitude} lon:{longitude}")
        return Response(status=status.HTTP_404_NOT_FOUND)
    # Try to get the list of services the call wants to use
    services = set(Services.objects.values_list("name", flat=True).distinct())

    use = request.GET.get('use', False)
    if use:
        use = set(use.split(','))
        services = services & use # yeah simple intersection, to keep things flat

    if not services:
        logger.warning("no valid option on {use}")
        return Response({"message": "No enough options selected"},
                        status=status.HTTP_400_BAD_REQUEST)

    # call each service on sequence and collect its result
    result = []
    for service in Services.objects.filter(name__in=services).filter(enabled=True).all():
        try:
            answer = service.process(latitude, longitude)
            result.append(answer)
        except ValueError:
            # for this excercise, just ignore bad values
            logger.warning(f"exception from {service.name}")
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


@api_view(['GET'])
def zipcode(requests, zipcode):
    return Response({"data":"Empty"})
