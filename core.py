import requests, humanize
from geopy.geocoders import Nominatim
from datetime import datetime
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange

class daily:   
    def forecast(place, time=None, date=None, forecast=None):
        try:
            date_time = datetime.now()
            if time == None:
                time = date_time.strftime("%H:%M:%S")
            if date == None:
                date = date_time.strftime("%Y-%m-%d")
            if forecast == None:
                forecast == "daily"
        except Exception as e:
            return("Exception occured with parameters format. Follow the format: Date (Y-m-d) and Time (H:M:S)")

        try:
            # convert place to lat and long
            geolocator = Nominatim(user_agent="forecast")
            location = geolocator.geocode(place)
            latitude = round(location.latitude, 2)
            longitude = round(location.longitude, 2)
        except Exception as e:
            print("Exception while fetching lat,long")

        try:
            # api endpoint to fetch 10 days data
            api_endpoint = f"https://api.weather.com/v2/turbo/vt1dailyForecast?apiKey=d522aa97197fd864d36b418f39ebb323&format=json&geocode={latitude}%2C{longitude}&language=en-IN&units=e"
            response = requests.get(api_endpoint)
            response_data = response.json()
        except Exception as e:
            print("Exception while accessing the API")

        try:
            # data wise data
            dates_time_list = response_data["vt1dailyForecast"]["validDate"]
            dates_list = [_.split("T0")[0] for _ in dates_time_list]
            # today's date index
            date_index = dates_list.index(date)
        except Exception as e:
            print("Please check the date format. [Y-m-d]")

        try:    
            temperature_day = response_data["vt1dailyForecast"]["day"]["temperature"][date_index]
            precipitate_day = response_data["vt1dailyForecast"]["day"]["precipPct"][date_index]
            uv_description_day = response_data["vt1dailyForecast"]["day"]["uvDescription"][date_index]
            wind_speed_day = response_data["vt1dailyForecast"]["day"]["windSpeed"][date_index]
            humidity_day = response_data["vt1dailyForecast"]["day"]["humidityPct"][date_index]
            phrases_day = response_data["vt1dailyForecast"]["day"]["phrase"][date_index] 
            narrative_day = response_data["vt1dailyForecast"]["day"]["narrative"][date_index]

            temperature_night = response_data["vt1dailyForecast"]["night"]["temperature"][date_index]
            precipitate_night = response_data["vt1dailyForecast"]["night"]["precipPct"][date_index]
            uv_description_night = response_data["vt1dailyForecast"]["night"]["uvDescription"][date_index]
            wind_speed_night = response_data["vt1dailyForecast"]["night"]["windSpeed"][date_index]
            humidity_night = response_data["vt1dailyForecast"]["night"]["humidityPct"][date_index]
            phrases_night = response_data["vt1dailyForecast"]["night"]["phrase"][date_index]
            narrative_night = response_data["vt1dailyForecast"]["night"]["narrative"][date_index]
            
            if temperature_day == None:
                forecast_data = f"Night\nTemp: {temperature_night}\nPrecipitate: {precipitate_night}\nUV Description: {uv_description_night}\nWind Speed: {wind_speed_night}\nHumidity: {humidity_night}\nPhrases: {phrases_night}\nNarrative: {narrative_night}"
            else:
                forecast_data = f"Day\nTemp: {temperature_day}\nPrecipitate: {precipitate_day}\nUV Description: {uv_description_day}\nWind Speed: {wind_speed_day}\nHumidity: {humidity_day}\nPhrases: {phrases_day}\nNarrative: {narrative_day}\n\nNight\nTemp: {temperature_night}\nPrecipitate: {precipitate_night}\nUV Description: {uv_description_night}\nWind Speed: {wind_speed_night}\nHumidity: {humidity_night}\nPhrases: {phrases_night}\nNarrative: {narrative_night}"
            return forecast_data

        except Exception as e:
            return "Exception while fetching data"

    def covid(place, type_of_place="country"):
        geolocator = Nominatim(user_agent="covid")
        location = geolocator.geocode(place)
        latitude = round(location.latitude, 2)
        longitude = round(location.longitude, 2)
        if type_of_place == "country":
            api_endpoint = f"https://api.weather.com/v3/wx/disease/tracker/country/1year?apiKey=d522aa97197fd864d36b418f39ebb323&format=json&geocode={latitude}%2C{longitude}"
        if type_of_place == "state":
            api_endpoint = f"https://api.weather.com/v3/wx/disease/tracker/state/1year?apiKey=d522aa97197fd864d36b418f39ebb323&format=json&geocode={latitude}%2C{longitude}"
        if type_of_place == 'county':
            api_endpoint = f"https://api.weather.com/v3/wx/disease/tracker/county/1year?apiKey=d522aa97197fd864d36b418f39ebb323&format=json&geocode={latitude}%2C{longitude}"
        r = requests.get(api_endpoint)
        pop = r.json()['covid19']['totalPopulation']
        cases = r.json()['covid19']['confirmed'][0]
        deaths = r.json()['covid19']['deaths'][0]
        death2cases = round((float(int(deaths)/int(cases))*100),2)
        covid_data = f"COVID Tracker\n\nLocation: {place} | Date: {datetime.today()}\n\nTotal Population: {humanize.intcomma(pop)}\nCases: {humanize.intcomma(cases)}\nDeaths: {humanize.intcomma(deaths)}\nDeath to Case Ratio: {death2cases}%"
        return covid_data

    def stocks(stock):
        key = "Q6L53I6MNEMHOZ4G"
        crypto = ["BTC", "ETH", "XMR"]
        if stock in crypto:
            fe = ForeignExchange(key=key)
            data, _ = fe.get_currency_exchange_rate(stock, "USD")
            full_price = data["5. Exchange Rate"]
            fp = f"${humanize.intcomma(float(full_price[:-2]), 2)}"
        else:
            ts = TimeSeries(key=key)
            data, meta_data = ts.get_intraday(stock)
            key = list(data.keys())[0]
            full_price = data[key]["1. open"]
            fp = f"${humanize.intcomma(float(full_price[:-2]), 2)}"
        return fp
