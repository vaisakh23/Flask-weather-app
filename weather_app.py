from flask import Flask, render_template, request, flash
from get_weather import GetWeather

app = Flask(__name__)
app.config["SECRET_KEY"] = "hejdjsjiddkjdjjdjdjsj"

previous_weather_data = GetWeather("London")

@app.route("/", methods=["GET", "POST"])
def home():
	global previous_weather_data
	wea_data = previous_weather_data
	# checking input
	if request.method == "POST":
		city = request.form.get("city")
		if len(city) > 1:
			new_wea_data = GetWeather(city)
		# getting weather data
		if new_wea_data.json:
			previous_weather_data = new_wea_data
			wea_data = new_wea_data
		else:
			flash("No result found")
	
	return render_template("index.html", wea_data=wea_data)

if __name__ == "__main__":
	app.run()