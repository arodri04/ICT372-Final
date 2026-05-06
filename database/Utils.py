import sqlite3
import hashlib
import string
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
import yfinance as yf
import random
import requests
from dataclasses import dataclass

#CLASSES
@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    temp: float



#FUNCTIONS
def connectDB():
    try:
        conn = sqlite3.connect('./instance/db.sqlite')
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to the database {e}")
        return None
    
def validateLogin(username, password):
    try:
        conn = connectDB()

        if not conn:
            return False
        
        cursor = conn.cursor()

        query = "SELECT salt, password FROM users WHERE username = ?"
        cursor.execute(query,(username,))
        result = cursor.fetchone()

        if result:
            salt, passHash = result
            combinePass = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
            if combinePass == passHash:
                return True          
        return False
    except sqlite3.Error as e:
        print(f"Database Error {e}")
        return False
    finally:
        if conn:
            conn.close()

def validateEmail(username):
    pattern ='^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    try:
        conn = connectDB()
        if not conn:
            return False 
        #Make sure that there isnt more emails
        cursor = conn.cursor()
        query = "SELECT 1 FROM users WHERE username = ?"
        cursor.execute(query,(username,))
        result = cursor.fetchone()
        #Make sure it is an email
        if not result:
            if re.fullmatch(pattern, username):
                return True
        return False
    except sqlite3.Error as e:
        print(f"Database Error {e}")
        return False
    finally:
        if conn:
            conn.close()


def saltShaker():
    characters = string.ascii_letters + string.digits
    salt = ''.join(random.choices(characters, k=5))
    return salt

    
def getUserId(username):
    try:
        conn = connectDB()
        if not conn:
            return False
        
        cursor = conn.cursor()
        query = "SELECT userId FROM users WHERE username = ?"
        cursor.execute(query,(username,))
        result = cursor.fetchone()
        if result:
            return result
            
        return False 
    except sqlite3.Error as e:
        print(f"Database Error {e}")
        return False  
    finally:
        if conn:
            conn.close()

#WEATHER FUNCTIONS

def getLatLon(cityName, stateCode, countryCode, WEATHER_KEY):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={cityName},{stateCode},{countryCode}&appid={WEATHER_KEY}"
    response = requests.get(url).json()
    data = response[0]
    lat, lon = data['lat'], data['lon']
    return lat, lon


def getFiveDayForecast(lat, lon, WEATHER_KEY):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={WEATHER_KEY}&units=imperial"
    response = requests.get(url).json()
    data = []

    for i in range(5):
        try:
            dayData = WeatherData(
                main=response['list'][i]["weather"][0]["main"],
                description=response['list'][i]['weather'][0]["description"],
                icon=response['list'][i]["weather"][0]['icon'],
                temp=response['list'][i]["main"]['temp']
            )
            data.append(dayData)
        except Exception as e:
            print(f"Error Making day data: {e}")
        
    
    return data

def getCurrentWeather(lat, lon, WEATHER_KEY):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_KEY}&units=imperial"
    response = requests.get(url).json()
    
    data = WeatherData(
        main=response['weather'][0]['main'],
        description=response['weather'][0]['description'],
        icon=response['weather'][0]['icon'],
        temp=response['main']['temp']
    )
    
    return data   

#NEWS FUNCTIONS

def getNews():
    url = "https://api.spaceflightnewsapi.net/v4/articles"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        articles = data.get('results', [])
        
        return articles
    else:
        print(f"Error: {response.status_code}") 
    
#STOCK FUNCTIONS

def getStocks():
    
    ticker = yf.Ticker("AAPL")
    monthlyData = ticker.history(period="6mo", interval="1mo")
    xValues = []
    yValues = []

    dfReset = monthlyData.reset_index()
    
    for month in dfReset['Date']:
        dateInterval = datetime.fromisoformat(str(month)).strftime("%m/%d/%Y")
        xValues.append(dateInterval)

    for month in monthlyData["Open"]:
        yValues.append(round(month, 2))
    
    print(xValues)
    print(yValues)

    return xValues, yValues


def randomTickers():
    spaceTickers = ["RKLB", "LUNR", "ASTS", "PL", "RDW", "VOYG", "SPIR", "FLY", "SPCE", "SATS", "IRDM", "LMT", "NOC", "BA", "LHX", "BKSY", "MNTS","SIDU"]
    data = []
    
    randomIndex = random.sample(range(len(spaceTickers)), k=5)
    for i in randomIndex:
        print(spaceTickers[i])

