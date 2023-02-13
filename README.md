Dockerised Weenat Test Backend

run:
    compose installed as docker plugin:
        docker-compose up --build

    compose installed as docker built-in:
        docker compose up --build

use:
http://localhost/docs

test:
docker exec backend pytest

descriptions of docker services:
- backend fastAPI service with 3 urls:
    - /api/ingest -> get request launch ingestion (see comment bellow) 
    - /api/summary -> get summarised data from db
    - /api/data -> get data from db

- database service:
PostGres db with one measurement model migrated at build from SQL ALchemy ORM
this is only for this test purpose but migration should be done manually.
we test inside the same db but it is clearly a bad practice.
In the right env, db test should be independent (init well choosed data in db_test and clean it after)

- datalogger service:
node.js webserver to expose data. readme was false, i corrected it

remarks:
- code formated by black isort pip plugins
- i'm fairly new with fastAPI, SQL alchemy, numpy, panda and pydantic.
- this projet is only for development purpose. For production, backend service should be route to nginx, .env.prod files should be created from the template for each services.Lighter containers. We should have a stronger password and escape characters in the url of sqlAlchemy connection...
- I added a 'raw' value inside span enums because this is the default value
- As you said, this test was simple so i went straight for the code. i wanted to show at least an orm implementation and an embeded env with docker.
because of that i fel in few issues:
    - the key of the measurement dict is not primary key (not unique)
    - the list received from json service has two positions with duplicated data inside. i wasn't sure about how to handle that
    - i went for a python alpine version but numpy needs a full one
    - i should have begun to type responses shema and field validation. after 2 full days on that i leave it like that but it's not proper at all. :(
        Pydantic is really powerfull i need more time to use it at it's best 

I spent 2 days on this : one day to dig into docs and configure and an other one for the api.

If i had more time:
- you asked a command to ingest data. i used an url. Maybe we could need to implement a bash function for ingestions.
    I use to develop on Django manage.py cmd and fast api dose'nt have an equivalent.
- find better way to serialize queryset from sqlalchemy
- use a schema template to automatically format respsonses
- properly resolved dependencies and install it with the higher version compatible
- managing cache in function of the ingestion frequency
- managing connnection with watchdogs and retries 
- install a logger
- go further with fast api , more error managing (field validation, connexions, ...),
    better error messages, better description for openapi's field ...
- go further into pydantic / typhint , type all the variables , specially the one returned by url
- go further into sql alchemy to a better, bind of model fields, connexion managing ...
- go further with panda and numpy. all parsing and filtering should work with those library but i didn't find the right function. i guess it exists 
    a way to parse and filter with a lambda on a list of dict to retrieve a dataset.
- go further in test with pytest and dispatch what is fonctional, integration, ... install coverage. mock all span values. i think the best is to have a coverage around 80% with smart test than a 100% with no meaning (test also errors on fields, datalogger, url, ...)