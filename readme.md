Game stats project 
==================

Django-based project with RESTful API for managing player stats.



Getting Started
---------------

These instructions will get you a copy of the project up and running on your local machine for development and testing 
purposes.

### Prerequisites

-   Python 3.x
-   pip



### Installing

1.  Clone the repository
2.  Create and activate a Python virtual environment (optional)
3.  Install the dependencies:

`pip install -r requirements.txt`

4. Rename files that hold sensitive data (remove _"\_template"_ from the file name):

`./exercise/secrets_template.py` into `./exercise/secrets.py`
`Rename ./docker_compose_template.yml` into `./docker_compose.yml`
`Rename ./init_template.sql` into `./init.sql`


5.  Create a Django secret key and paste it in `pokemon/secrets.py`, as the SECRET_KEY value, replacing 
`your Django secret key here` with it: 

`python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

6. Replace with your desired values in the following files:

`./exercise/secrets.py`, `./docker_compose.yml` and `./init.sql`

You should replace:
```
mysql_root_password
mysql_database
mysql_user
mysql_password
```

7. Run the docker container:
`docker-compose up -d --build`


8. Apply migrations:
`python manage.py migrate`



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

`celery -A exercise worker --loglevel=DEBUG`

Please note: if running in Windows: add " -P solo" at the end of worker command:
`celery -A exercise worker --loglevel=DEBUG -P solo`

All 3 must run simultaneously. Redis must also be running and shouldn't need to be manually run, as the Redis server 
is started as part of the Docker container initialization.





Access the API
--------------

Run the server:

`python manage.py runserver`

The app should now be accessible at <http://localhost:8000> (unless a different port is specified).


### Django admin console

First add a super user:

`python manage.py createsuperuser`

And select the user name and password of your preference.

Once the server is running, an admimn console UI will be available through http://localhost:8000/admin/



### REST Client (e.g.: Postman)

See the _Endpoints_ section.



Endpoints
---------

Swagger documentation is available at http://localhost:8000/game_stats/schema/swagger-ui/ (project must be running) 
and a downloadable yaml file is available at http://localhost:8000/game_stats/schema/.

### Overview

Pagination is enabled (defaults to 10 items per page). 

* `/players/`: GET, POST. (E.g.: http://localhost:8000/players/)
To use pagination, add: `?page=X` (where X is the page number) as a parameter (E.g.: 
http://localhost:8000/players?page=3).

* `/players/{id}/`: GET, PUT, PATCH, DELETE (E.g.: http://localhost:8000/players/21)

* `/games/`: GET, POST. (E.g.: http://localhost:8000/games/)
To use pagination, add: `?page=X` (where X is the page number) as a parameter (E.g.: 
http://localhost:8000/games?page=3).

* `/games/{id}/`: GET, PUT, PATCH, DELETE (E.g.: http://localhost:8000/games/21)

* `/stats/`: GET, POST. (E.g.: http://localhost:8000/stats/)
To use pagination, add: `?page=X` (where X is the page number) as a parameter (E.g.: 
http://localhost:8000/stats?page=3).

* `/stats/{id}/`: GET, PUT, PATCH, DELETE (E.g.: http://localhost:8000/stats/21)


### Resources


1. Player (endpoint: **/players/**)

* `id`: Autonumeric field that represents the primary key in the database. Read-only field.
* `nickname`: Player nickname (e.g.: "test_user") that can only contain letters, numbers or underscores. Required field.
* `profile_image`: An URL containing a profile image (avatar) of the player. Optional field.

2. Game (endpoint: **/games/**)

* `id`: Autonumeric field that represents the primary key in the database. Read-only field.
* `players`: Players involved in the game (0-10 players). A list of foreign keys to the *Player* model.
* `winner`: The game winner. A foreign key to the *Player* model. Must be included in the players list. Optional field.

3. Stat (endpoint: **/stats/**)

* `id`: Autonumeric field that represents the primary key in the database. Read-only field.
* `player`: The player associated to the stat. A foreign key to the *Player* model. Required field.
* `creation_date`: Date of card creation. Automatically defaults to the current date of entry. Read-only field.
* `score`: The score obtained by the player. Must be a positive number. Optional field.
* `game`: The game associated to the stat. A foreign key to the *Game* model. Optional field.




Running unit tests
-----------------

To run all tests, execute:

`python manage.py test game_stats.tests --pattern="*_test.py"`

To run a specific test file (by replacing `<module>` and `<file>`):

`python manage.py test game_stats.tests.<module>.<file>`

Test files are placed in the `./game_stats/tests/` folder


Migrations
----------

Should you make any changes to the model, migrations might be needed to update the database:

`python manage.py makemigrations`

`python manage.py migrate`
