from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import getenv, environ

app = Flask(__name__)



if getenv('enviroment') == "dev":
    app.config.from_object("config.Development")
elif getenv('enviroment') == "prod":
    app.config.from_object("config.Production")
else:
    raise Exception('No enviroment set')


db = SQLAlchemy(app)


from app.views import view
from app.models.tables import WeatherData

