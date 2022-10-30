import requests
import json
from datetime import datetime
import pytz

API_KEY = "b4c4ada6a2c91b2a126721df62de169d"
URL = "https://api.openweathermap.org/data/2.5/"

class GetWeather:
	def __init__(self, city):
		self.city = city
		self.geo_json = self.get_geocode()
		self.json = self.get_json()
		if self.json:
			self.time_zone = self.get_time_zone()
			self.weather = self.get_weather()
			self.icon_name = self.get_weather_icon()
			self.date_time = self.get_date_time()
			self.location = self.get_location()
			self.day_forcast = self.get_day_forcast()
			self.forcast = self.get_forcast()

				
	def get_geocode(self):
		"""
		'current weather data' api call for
		geocoding
		"""
		try:
			url = URL + f"weather?q={self.city}&appid={API_KEY}"
			data = requests.get(url).text
			return json.loads(data)
		except:
			print("error")
		return
						
	def get_json(self):
		"""
		'one call api' call for weather details
		"""
		if  not self.geo_json:
			return None
		try:
			lon , lat = self.geo_json["coord"]["lon"], self.geo_json["coord"]["lat"]
			url = URL + f"onecall?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&exclude=minutely,alerts"
			api_data = requests.get(url).text		
			return json.loads(api_data)
		except:
			print("error")
		return
		
	def get_weather(self):
		temp = round(self.json["current"]["temp"])
		feels_like = round(self.json["current"]["feels_like"])
		pressure = self.json["current"]["pressure"]
		wind = round(self.json["current"]["wind_speed"],1)
		humidity = self.json["current"]["humidity"]
		visibility = round((self.json["current"]["visibility"])/1000, 1)
		uv = round(self.json["current"]["uvi"], 1)
		min_temp = round(self.json["daily"][0]["temp"]["min"])
		max_temp = round(self.json["daily"][0]["temp"]["max"])
		
		ri_dt = self.json["current"]["sunrise"]
		sunrise = datetime.fromtimestamp(ri_dt, tz=self.time_zone)
		st_dt = self.json["current"]["sunset"]
		sunset = datetime.fromtimestamp(st_dt, tz=self.time_zone)
																		
		weather = {
		"temp": f"{temp}°C",
		"feels like": f"{feels_like}°C", 
		"description": self.json["current"]["weather"][0]["description"],
		 "pressure": f"{pressure}hpa", 
		 "wind speed": f"{wind}m/s", 
		 "humidity": f"{humidity}%", 
		 "visibility": f"{visibility}km",
		 "uv": f"{uv}",
		 "min": f"{min_temp}°",
		 "max": f"{max_temp}°",
		 "sunrise":sunrise.strftime("%-I:%M %p"),
		 "sunset": sunset.strftime("%-I:%M %p")
		 }
		return weather
	
	def get_weather_icon(self):
		icon = self.json["current"]["weather"][0]["icon"]
		return icon
	
	def get_time_zone(self):
		time_zone = pytz.timezone(self.json["timezone"])
		return time_zone
	
	def get_date_time(self):
		dt = datetime.now(tz=self.time_zone)
		return dt.strftime("%a %-d %b %-I:%M %p")
	
	def get_location(self):
		country = self.geo_json["sys"]["country"]
		return f"{self.city},{country}"
		
	def scrap_temp(self, temp_type):
		# helper funtion
		data = []
		for i in range(1, 7):
			temp_data = round(self.json["daily"][i]["temp"][temp_type])
			data.append(f'{temp_data}°C')
		return data
	
	def get_day_forcast(self):
		# daily forcast  data
		forcast = {"day": [], "temp": [], "icon": []}
		for i in range(1, 7):
			day = self.json["daily"][i]["dt"]
			dt = datetime.fromtimestamp(day)
			forcast["day"].append(dt.strftime("%a"))
			
			icon_id = self.json["daily"][i]["weather"][0]["icon"]
			forcast["icon"].append(icon_id)
					
		forcast["temp"] = self.scrap_temp("day")
		return forcast
	
	def get_forcast(self):
		# hourly forecast
		forcast = {"time": [], "temp": [], "icon": []}
		for i in range(1, 7):
			day = self.json["hourly"][i]["dt"]
			dt = datetime.fromtimestamp(day)
			forcast["time"].append(dt.strftime("%-I:%M %p"))
			
			temp_data = round(self.json["hourly"][i]["temp"])
			forcast["temp"].append(f'{temp_data}°C')
			
			icon_id = self.json["hourly"][i]["weather"][0]["icon"]
			forcast["icon"].append(icon_id)
			
		return forcast
		

if __name__ == "__main__":
	wea = GetWeather("london")
	#print(wea.geocode.address)
	print(json.dumps(wea.json, indent=4))
	if wea.json:
		print(wea.weather)
		print(wea.icon_name)
		print(wea.date_time)
		print(wea.location)
		print(wea.day_forcast)
		print(wea.forcast)
	
	
	
