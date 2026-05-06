from flask import Flask, render_template as rt, request, redirect, url_for, session
from datetime import timedelta, date
from database.database import db
from database.models import *
from database.Utils import *
from dotenv import load_dotenv
import hashlib
import os



load_dotenv()
WEATHER_KEY = os.getenv('WEATHER_KEY')
FORECAST_KEY = os.getenv('FORECAST_KEY')
app = Flask(__name__)
app.secret_key = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


#All the routes for the app are here
@app.route('/')
def home():
    #If there is no session populate with none
    if session:
        user = session['user']
        articles = getNews()
        lat, lon = getLatLon('Albuquerque', 'NM', "US", WEATHER_KEY)
        getCurrentWeather(lat, lon, WEATHER_KEY)
        
    else:
        user = None 
        articles = None
    return rt('base.html', user=user, articles=articles)

@app.route('/news')
def news():
    #If there is no session populate with none
    if session:
        user = session['user']
        articles = getNews()
    else:
        user = None 
        articles = None
    return rt('news.html', user=user, articles=articles)

@app.route('/weather', methods=["GET","POST"])
def weather():
    if session:
        if request.method =="POST":
            user = session['user']
            city = request.form.get('city')
            state = request.form.get('state')
            country = request.form.get('country')
            try:
                lat, lon = getLatLon(city, state, country, WEATHER_KEY)
                weather = getCurrentWeather(lat, lon, WEATHER_KEY)
                forecast = getFiveDayForecast(lat, lon, FORECAST_KEY)
                
                return rt("weather.html", weather=weather, forecast=forecast, user=user, city=city, state=state, country=country)
            except:
                error = "Could not get data"
                return rt("weather.html", error=error, user=user, city="", state="", country="")  
        
        else:
            user = session['user']
            city = "Albuquerque"
            state = "NM"
            country = "US"
            lat, lon = getLatLon('Albuquerque', 'NM', "US", WEATHER_KEY)
            weather = getCurrentWeather(lat, lon, WEATHER_KEY)
            
            return rt("weather.html", weather=weather, user=user, city=city, state=state, country=country)
    else:
        return rt("login.html", error="Please Log In")
        
@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get('email')
        password = request.form.get('password')
        #Check DB for user
        if validateLogin(username, password):
            session['user'] = username
            session['userId'] = getUserId(username)[0]
            return redirect(url_for("home"))
        else:
            return rt("login.html", error="Invalid Login")
        
    return rt("login.html")       

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get('email')
        password = request.form.get('password')
        #Make sure an email address was sent
        if validateEmail(username):
            #salt the password
            salt = saltShaker()
            hashPass = hashlib.sha256((password+salt).encode('utf-8')).hexdigest()
            
            new_user = Users(username=username, password=hashPass, salt=salt)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))
        return rt("register.html", error="Could Not Validate Email.")

        
    return rt("register.html")    




if __name__ == '__main__':
    app.run(debug=True)