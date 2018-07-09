# Knowhere
Web app providing ability to upload huge data sets to the cloud from anywhere with an internet connection. Also allows data visualization and debugging.

Built with Django, Celery asynchronous task manager, RabbitMQ, Redis, D3.js, Bootstrap, and other tech.

Code edited and anonymized to preserve confidentiality and protect IP of customer. 

## Setting it up

https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04
^ helps. but not all steps are valid so pay attention

###If installing locally:
- ensure that the correct python 3 is installed; 3.6 or higher is recommended
- ensure that pip3 is installed
- pip3 install --upgrade pip
- pip3 install virtualenv
- clone project into folder
- cd into folder
- `virtualenv env`
- `source env/bin/activate` this gets you into the virtualenv
* NOTE that once you are in the env, you drop using pip3 and only use regular pip
- `pip install -r requirements.txt`
- grab the right settings.py from somewhere and copy it into the correct folder
- `python manage.py runserver` should run the server locally, which will provide everything EXCEPT for async task capabilities. To do that, you will need to run a celery worker locally as well.


###If installing on a server:
- set up non-root sudo user & log in as them
- `sudo apt-get update`
- `sudo apt-get install python3-pip python3-dev libpq-dev nginx`
- `sudo -H pip3 install --upgrade pip`
- `sudo -H pip3 install virtualenv`
- clone project into folder
- cd into folder
- `virtualenv env`
- `source env/bin/activate`
- `pip install -r requirements.txt`
- `pip install gunicorn`
- grab the right settings.py from somewhere and copy it into the correct folder
- create gunicorn systemd service file
- configure nginx to proxy pass to gunicorn by creating sites-available file and simlinking to sites-enabled
- restart nginx
- `sudo ufw allow 'Nginx Full'`
- https://stackoverflow.com/questions/24453388/nginx-reverse-proxy-causing-504-gateway-timeout
