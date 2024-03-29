Game stats project 
==================

Django-based project for managing player and game stats.

Test data can be populated into the database using the command provided. Alternatively, this can be done automatically 
using Celery and Redis.

MySQL and Redis run in Docker containers.

The top 10 players are listed in a web page that auto-refreshes every 10 seconds and allows to download data as a csv 
file. 

Django-Rest-Framework was used to create the RESTful API that enables managing players and games.


### Index

- [Project Description](#project-description)

- [Getting Started](#getting-started)

    - [Prerequisites](#prerequisites)
 
    - [Project installation and configuration](#project-installation-and-configuration)

- [Populate data](#populate-data)

    - [Manually](#manually)

    - [Automated](#automated)

- [Access data](#access-data)

    - [Django admin console](#django-admin-console)

    - [REST Client (e.g.: Postman)](#rest-client-eg-postman)

    - [HTML report for top 10 scores](#html-report-for-top-10-scores)

- [Endpoints](#endpoints)

    - [Overview](#overview)

    - [Resources](#resources)

- [Running unit tests](#running-unit-tests)

- [Migrations](#migrations)


-------------------
Project Description
-------------------

This project allows storing and managing statistics for a hypothetical game with multiple players. The game can have 
matches ("games") involving 0 to 10 players. This project generates statistics and a web report with the top 10 player 
scores.

Models are: _Player_ (a single player), _Game_ (a match that can have up to 10 players or even no players, for example 
if the match was abandoned by the players or was never started) and _Stat_ (statistics on a single player, that can 
optionally be related to a game but not necessarily, for example if general statistics or media scores need to be 
generated). More details on models can be found in the [Resources](#resources) section.


---------------
Getting Started
---------------

These instructions will get you a copy of the project up and running on your local machine for development and testing 
purposes.

### Prerequisites

- Python 3.x
- Docker


### Project installation and configuration

1.  Clone the repository
2.  Create and activate a Python virtual environment (optional)
3.  Install the dependencies:

`pip install -r requirements.txt`

4. Rename files that hold sensitive data (remove _"\_template"_ from the file name):

`./exercise/secrets_template.py` into `./exercise/secrets.py`

`./docker_compose_template.yml` into `./docker_compose.yml`

`./init_template.sql` into `./init.sql`

5. Replace with your desired values in the following files:

`./exercise/secrets.py`, `./docker_compose.yml` and `./init.sql`

You should replace:
```
mysql_root_password
mysql_database
mysql_user
mysql_password
```


6.  Create a Django secret key and paste it in `exercise/secrets.py`, as the SECRET_KEY value, replacing 
`your Django secret key here` with it: 

`python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`


7. Run the docker containers:

`docker-compose up -d --build`


8. Apply migrations:

`python manage.py migrate`


9. Generate static files

`python manage.py collectstatic`


-------------
Populate data
-------------

### Manually
You can populate the database with some random data by running the `simulate_stats.py` script:

`python manage.py simulate_stats`

This will make use of the <https://randomuser.me/api/> API to generate player data.


### Automated 

To run the previous script automatically using Celery and Redis:

1. Start server:

`python manage.py runserver`

2. Start celery beat:

`celery -A exercise beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler`

3. Start worker:

`celery -A exercise worker --loglevel=DEBUG -P solo`

All 3 must run simultaneously. Redis must also be running and shouldn't need to be manually run, as the Redis server 
is started as part of the Docker container initialization.

To modify the cron job that runs the script automatically, find the following line in the periodic task setting:

`'schedule': crontab(minute='*/5')`



-----------
Access data
-----------

Run the server:

`python manage.py runserver`

The app should now be accessible at http://localhost:8000 (unless a different port is specified).


### Django admin console

First add a super user:

`python manage.py createsuperuser`

and select the user name and password of your preference.

Once the server is running, an admimn console UI will be available through /admin/ (e.g.: http://localhost:8000/admin/).


### REST Client (e.g.: Postman)

See the _Endpoints_ section.


### HTML report for top 10 scores

View /ranking/ (e.g.: http://localhost:8000/ranking/). Stats will refresh every 10 seconds.

Optionally, the page includes a button to download this report as a csv file. 


---------
Endpoints
---------

Swagger documentation is available at http://localhost:8000/game_stats/schema/swagger-ui/ (project must be running) 
and a downloadable yaml file is available at http://localhost:8000/game_stats/schema/.


### Overview

Pagination is enabled (defaults to 10 items per page). 


* `/api/token/`: GET (e.g.: http://localhost:8000/api/token/). Log in with username and password (returns an access 
and refresh JWT pair).

* `/api/token/refresh/`: GET (e.g.: http://localhost:8000/api/token/refresh/). Refresh JSON web token (returns an 
access type token).

* `/players/`: GET, POST. (e.g.: http://localhost:8000/players/)
To use pagination, add: `?page=X` (where X is the page number) as a parameter (e.g.: 
http://localhost:8000/players?page=3).

* `/players/{id}/`: GET, PUT, PATCH, DELETE (e.g.: http://localhost:8000/players/21). Only admin users can delete.

* `/games/`: GET, POST. (e.g.: http://localhost:8000/games/)
To use pagination, add: `?page=X` (where X is the page number) as a parameter (e.g.: 
http://localhost:8000/games?page=3).

* `/games/{id}/`: GET, PUT, PATCH, DELETE (e.g.: http://localhost:8000/games/21). Only admin users can delete.

* `/stats/`: GET, POST. (e.g.: http://localhost:8000/stats/)
To use pagination, add: `?page=X` (where X is the page number) as a parameter (e.g.: 
http://localhost:8000/stats?page=3).

* `/stats/{id}/`: GET, PUT, PATCH, DELETE (e.g.: http://localhost:8000/stats/21). Only admin users can delete.

* `/stats/ranking/`: GET (E.g.: http://localhost:8000/stats/ranking/). Shows the 10 best scores of all time.

* `/users/`: GET, POST. (e.g.: http://localhost:8000/users/). To use pagination, add: `?page=X` (where X is the page 
number) as a parameter (e.g.: http://localhost:8000/users?page=3).

* `/users/{id}/`: GET, PUT, PATCH, DELETE (e.g.: http://localhost:8000/users/21). Only admin users can delete.



### Resources


1. User signup (endpoint: **/signup/**)
Model provided by django.contrib.auth component (https://docs.djangoproject.com/en/4.2/ref/contrib/auth/).
* `id`: Autonumeric field that represents the primary key in the database. Read-only field.
* `username`: User registration name. A string with 150 characters or fewer. Required field.
* `email`: User email. Optional field.
* `password`: User password. Required field.
* `first_name`: User first name. A string with 150 characters or fewer. Optional field.
* `last_name`: User last name. A string with 150 characters or fewer. Optional field.

2. Player (endpoint: **/players/**)

* `id`: Autonumeric field that represents the primary key in the database. Read-only field.
* `user`: An existing user. A foreign key to the *User* model. Required field.
* `nickname`: Player nickname (e.g.: "test_user") that can only contain letters, numbers or underscores. Required field.
* `profile_image`: An URL containing a profile image (avatar) of the player. Optional field.


3. Game (endpoint: **/games/**)

* `id`: Autonumeric field that represents the primary key in the database. Read-only field.
* `players`: Players involved in the game (0-10 players). A list of foreign keys to the *Player* model.
* `winner`: The game winner. A foreign key to the *Player* model. Must be included in the players list. Optional field.

4. Stat (endpoint: **/stats/**)

* `id`: Autonumeric field that represents the primary key in the database. Read-only field.
* `player`: The player associated to the stat. A foreign key to the *Player* model. Must be included in the player's 
list of the *game* field. Required field.
* `creation_date`: Date of card creation. Automatically defaults to the current date of entry. Read-only field.
* `score`: The score obtained by the player. Must be a positive number. Optional field.
* `game`: The game associated to the stat. A foreign key to the *Game* model. Optional field.





-----------------
Running unit tests
-----------------

To run all tests, execute:

`python manage.py test game_stats.tests --pattern="*_test.py"`

To run a specific test file (by replacing `<module>` and `<file>`):

`python manage.py test game_stats.tests.<module>.<file>`

Test files are placed in the `./game_stats/tests/` folder


----------
Migrations
----------

Should you make any changes to the model, migrations might be needed to update the database:

`python manage.py makemigrations`

`python manage.py migrate`
