# coding=utf-8
from flask import Flask,request,make_response
import os,json
import pyowm
import os

app = Flask(__name__)
owmapikey=os.environ.get('OWMApiKey') #or provide your key here
owm = pyowm.OWM(owmapikey)

#geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))
    
    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#processing the request from dialogflow
def processRequest(req):
    
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    metadata = result.get("metadata")
    intent = metadata.get("intentName")
    observation = owm.weather_at_place(city)
    w = observation.get_weather()
    latlon_res = observation.get_location()
    lat=str(latlon_res.get_lat())
    lon=str(latlon_res.get_lon())
     
    wind_res=w.get_wind()
    wind_speed=str(wind_res.get('speed'))

    cloud_result = w.get_clouds()
<<<<<<< HEAD
    #cloud = str(cloud_result.get('name'))
    cloud = cloud_result
=======
    cloud = str(cloud_result.get('name'))
>>>>>>> 30c06a0763f7f0083dbbc45fec6619962c5c5eba
    
    humidity=str(w.get_humidity())

    celsius_result=w.get_temperature('celsius')
    temp_celsius=str(celsius_result.get('temp'))

    fahrenheit_result=w.get_temperature('fahrenheit')
    temp_min_fahrenheit=str(fahrenheit_result.get('temp_min'))
    temp_max_fahrenheit=str(fahrenheit_result.get('temp_max'))

<<<<<<< HEAD
    if intent == "weather" :

        speech = "Today the weather in "+city+" is" +cloud+"% coverage"+" And the temperature is"+temp_celsius+"°C"

=======
    speech = "Today the weather in "+city+" is"+cloud+". And the temperature is"+temp_celsius
    
>>>>>>> 30c06a0763f7f0083dbbc45fec6619962c5c5eba
    return {
        "speech": speech,
        "displayText": speech,
        "source": "dialogflow-weather-by-mbbartnik"
        }
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
