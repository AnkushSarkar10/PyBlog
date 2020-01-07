# Py-blog

[The app](https://py-bl0g.herokuapp.com/home)

## Built With

* [Flask](http://flask.palletsprojects.com/en/1.1.x/) - The python web framework used
* [Flask-sql-alchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) - For Database Management
* [Flask-Dance](https://flask-dance.readthedocs.io/en/latest/) and [Flask-Login](https://flask-login.readthedocs.io/en/latest/) - Used to create the login system.
* [Flask-Wtf](https://flask-wtf.readthedocs.io/en/stable/) - For The web forms.
* A [Postgress](https://www.postgresql.org/) database is used.

other dependencies are in the _requirements.txt_. 

## Deployment

We used [Heroku](https://www.heroku.com/) for hosting our site.

## Code
* [views.py](app/views.py) - This has all the routs to the differnt sections of the site, and also the login infos.
* [models.py](app/models.py) - This has the classes used to create the slq-alchemy data bases
* [forms.py](app/forms.py) - This has the form classes created by wt-forms.
* [Templates](app/html) - This contains all the __html__ code.
* [Static](app/Static/css) -  This contains all the __css__ code.
* [run.py](run.py) - It runs the app.

## Credit
__Ankush Sarkar__
__Soham Mondal__
__Alan Thomas__
__Tanuj Adhikary__
