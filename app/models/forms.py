from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired


lang_choices = [("pt-br","Português"),("en","Ingles"),("es","Espanhol"),('de','German'),('fr','French')]
units_choices = [("metric","Celsius"),("standard","Kelvin"),("imperial","Fahrenheit")]

class WeatherForm(FlaskForm):
    place = StringField('Localização',validators=[DataRequired()])
    units = SelectField('Unidade de medida',choices=units_choices)
    button = SubmitField("Enviar") 