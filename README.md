# Contact Tracing Project

## Project Setup

##### Local Runserver

1. Create a virtualenv running on 3.8.2
2. Install PostgreSQL and create a database for the project
3. Clone the project
4. Run the command `pip install -r requirements.txt` to install local environment apps
5. Create a copy of `contact_tracing/settings/local.tpl` and rename the copy to `local.py`
6. Edit `local.py` settings to match your local environment setup
7. Migrate the database using the command `python manage.py migrate`
8. Run the app using `python manage.py runserver`
