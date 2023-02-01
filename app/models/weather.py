import requests
from dotenv import load_dotenv
from os import getenv
from geopy import Nominatim
from datetime import datetime, time
from timezonefinder import TimezoneFinder as tf
from pytz import timezone as tz


load_dotenv()

class CurrentWeather:
    api_key = getenv('weather_key')

    def __init__(self,place,lang,units) -> None:
        self.place = place    
        self.lang =lang.replace('-','_')
        self.units = units

    def kelvinToCelsius(self,k):
        resultado =  round(k - 273.15,0)

        return str(int(resultado)) + 'ºC'
        
    def getLocation(self):

        locator = Nominatim(user_agent="myGeocoder")
        location = locator.geocode(self.place)
        self.lat = location.latitude
        self.lon = location.longitude


    def getTimeZone(self):
        dt = tf().timezone_at(lat=self.lat,lng=self.lon)
        timezone = tz(dt)

        return datetime.now(timezone)

    def transformDate(self,date):
        
        if isinstance(date,int):
            date = datetime.fromtimestamp(date)

        if isinstance(date,str):
            date = datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
        

        weekday_name =  ["Segunda-Feira", "Terça-Feira", "Quarta-Feira", "Quinta-Feira", "Sexta-Feira", "Sabado", "Domingo"]
        month_name = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
        mesNome = month_name[date.month-1]

        return {
                'dateHour': f"{date.day}/{mesNome}/{date.year} {date.time().strftime('%H:%M:%S')}",
                'monthName': weekday_name[date.weekday()]
                }

    def getData(self,res):

        def condition(key):
            tmp = {}

            if key in res.keys():
                rain = res[key]
                if '1h' in rain.keys():
                    tmp[key + '_1h'] = rain['1h']
                if '3h' in rain.keys():
                    tmp[key + '_3h'] = rain['3h']

            return tmp

        myList = {}


        for key in res.keys():
            #python 3.9
            # if key not in ['rain','snow']:
            #     if isinstance(res[key],list):
            #         myList = myList | res[key][0] 
            #     elif isinstance(res[key],dict):
            #         myList =  myList | res[key]
            #     else:  
            #         myList[key] = res[key]
            
            #python 3.7
            if key not in ['rain','snow']:
                if isinstance(res[key],list):
                    myList = {**myList, **res[key][0]}
                elif isinstance(res[key],dict):
                    myList = {**myList,**res[key]}
                else:  
                    myList[key] = res[key]




        rain = condition('rain')
        snow = condition('snow')

        #python 3.9
        # if bool(rain):
        #     myList = myList | rain

        # if bool(snow):
        #     myList = myList | snow

        #python 3.7
        if bool(rain):
            myList = {**myList,**rain}

        if bool(snow):
            myList = {**myList,**snow}

        return myList

    def niceDict(self,data):
       

        bDict = {}
        
        if self.units == "metric":
            metrica = " ºC"
        elif self.units == "standard":
            metrica = " ºK"
        else:
            metrica = " ºF"
        
        niceLabels = ['Titulo','Descricao','icon','Temperatura atual','Sensacao termica','Temperatura minima','Temperatura maxima','Temperatura parametro interno','Pressao atmosferica','Pressao atmosferica nos oceanos','Pressao atmosferica na terra','Visibilidade','Velocidade dos ventos','Direcao dos ventos','Rajada de vento','Nuvens','Volume de chuva nas ultimas 1h','Volume de chuva nas ultimas 3h','Volume de neve nas ultimas 1h','Volume de neve nas ultimas 3h','Nascer do sol','Por do sol','Pais','Localidade','Umidade','id','Probabilidade de chuver']
        oldLabels = ['main','description','icon','temp','feels_like','temp_min','temp_max','temp_kf','pressure','sea_level','grnd_level','visibility','speed','deg','gust','all','rain_1h','rain_3h','snow_1h','snow_3h','sunrise','sunset','country','name','humidity','id','pop']


        for key in data:
            try:
                if key in ['temp','feels_like','temp_min','temp_max']:
                    bDict[niceLabels[oldLabels.index(key)]] = str(round(data[key],2)) + metrica
                elif key in ['pressure','sea_level','grnd_level']:
                    bDict[niceLabels[oldLabels.index(key)]] = str(data[key]) + " pHA"
                elif key in ['visibility']:
                    bDict[niceLabels[oldLabels.index(key)]] = str(data[key]) + "m"
                elif key in ['speed','gust']:
                    bDict[niceLabels[oldLabels.index(key)]] = str(data[key]) + " m/s"
                elif key in ['deg']:
                    bDict[niceLabels[oldLabels.index(key)]] = str(data[key]) + "°"
                elif key in ['all']:
                    bDict[niceLabels[oldLabels.index(key)]] = str(data[key]) + "%"
                elif key in ['sunrise','sunset']:
                    bDict[niceLabels[oldLabels.index(key)]] = datetime.fromtimestamp(data[key]).time()
                elif key == 'dt':
                    dateHour,weekName = self.transformDate(data[key]).values()
                    bDict['Data e hora atual'] = dateHour
                    bDict['Dia nome'] = weekName
                    bDict['Data e hora local'] = self.transformDate(self.getTimeZone())['dateHour']
                elif key == 'dt_txt':
                    dateHour,weekName =  self.transformDate(data['dt_txt']).values()

                    bDict['Data e hora previsao'] = dateHour
                    bDict['Dia nome previsao'] = weekName

                else:
                    bDict[niceLabels[oldLabels.index(key)]] = str(data[key])
            except:
                pass


        bDict['latitude'] = self.lat
        bDict['longitude'] = self.lon

        return bDict



    def getweather(self):
        
        self.getLocation()
       
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={self.api_key}&units={self.units}&lang={self.lang}"
        res = requests.get(url).json()

        self.all = self.getData(res) 

        return self.all

    def start(self):
        try:
            self.getweather()
            return self.niceDict(data=self.all),'Sucesso'
        except Exception as e: 
            return None,e


class forecastWeather(CurrentWeather):
    def getForcast(self):

        self.getLocation()

        url = f"http://api.openweathermap.org/data/2.5/forecast?lat={self.lat}&lon={self.lon}&appid={self.api_key}&units={self.units}&lang={self.lang}"
        res = requests.get(url).json()['list']
        self.all = []

        alone = ['dt_txt','pop']
       
        for element in res:
            tmp = {}

            for key in element.keys():
                if key in ['main','weather','rain','snow','wind']:
                    tmp[key] = element[key]
                elif key in alone:
                    tmp[alone[alone.index(key)]] = element[key]
                else:
                    pass
    

            self.all.append(self.getData(tmp))
        
        return self.all

    def niceDictList(self):
        bDict = []

        for element in self.all:
            bDict.append(self.niceDict(data=element))

        return bDict
    

    def forecastDay(self):
        self.getForcast()
        dt = self.niceDictList()
        dt_final = []
        for element in dt:
            if element['Data e hora previsao'].endswith('06:00:00'):
                dt_final.append(element)

        
        return dt_final

    def startForecast(self):
        
        self.getForcast()
        return self.niceDictList()




if __name__ == "__main__":
    #el = CurrentWeather( "marica", "pt-br",units='metric').getweather()
    el = forecastWeather( "Dundee Reino unido", "pt-br",'metric').startForecast()
    #el = forecastWeather( "Dundee Reino unido", "pt-br",'metric').getForcast()
    print(el[0])