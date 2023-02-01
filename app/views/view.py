from app import app
from flask import render_template,request,flash
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
    
    if request.method == "POST":
        
        data,mensagem = CurrentWeather(place = form.data['place'],lang= 'pt-br',units=form.data['units']).start()
        if data is not None:
            return render_template('index.html',form = form,data=data)

        flash(f"Não encontrado o endereço informado,{mensagem}",category="warning")
      
        
    return render_template('index.html',form = form)

@app.route('/previsao',methods=['GET',"POST"])
def test():
    form = WeatherForm()

    if request.method == "POST":
        try:
            data = forecastWeather(place = form.data['place'],lang= 'pt-br',units=form.data['units']).forecastDay()
            return render_template('previsao.html',form=form,data=data)
        except:
            flash("Não encontrado o endereço informado",category="warning")

    return render_template('previsao.html',form=form)