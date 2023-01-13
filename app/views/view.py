from app import app
from flask import render_template,request
from app.models.forms import WeatherForm
from app.models.weather import CurrentWeather, forecastWeather
from googletrans import Translator


@app.template_filter('translate')
def translate(text,dest):
    if dest == "pt-br":
        return text

    translator = Translator()
    translation = translator.translate(text,dest=dest)
    return translation.text




@app.route('/',methods = ["GET","POST"])
def main():
    form = WeatherForm()
    data = None
    
    if request.method == "POST":
 
        data = CurrentWeather(place = form.data['place'],lang= 'pt-br',units=form.data['units']).start()
      
        

    return render_template('index.html',form = form,data=data)

@app.route('/previsao',methods=['GET',"POST"])
def test():
    form = WeatherForm()
    data = None

    if request.method == "POST":

        data = forecastWeather(place = form.data['place'],lang= 'pt-br',units=form.data['units']).startForecast()
        print(data[0])

    return render_template('previsao.html',form=form,data=data)