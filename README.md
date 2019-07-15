# sw-ICC
ShipWell - Initial Code Challenge (BE)


You need to have installed docker and docker-compose

once you have it installed, then run the following:

create an ".env" file to setup the following:

	DEBUG=on
	GOOGLE_MAPS_API_KEY=<google maps api key>

it should go to wetaher directory.

$ docker-compose buil
$ docker-compose run web python manage.py migrate
$ docker-compose run web python manage.py loaddata init.json
$ docker-compose up


this will start the application on localhost:8000

so the url to handle is:

http://localhost:8000/<longitude>/<latitude>/

also you have ?use= as a way to pass what entries you what to use

in the same way on 

http://localhost:8000/admin/temperature/

you can find the list of services defined in the system

user: admin
password: sesam0.1

or if you want you can create a new superuser by:

$ docker-compose run web python manage.py createsuperuser

Julio.
