#!/bin/python3

import json
import turtle
import time
from urllib.request import urlopen

# Interface to pull results from web api
def web_service_interface(url, lat = 0, lon = 0):
    if (lat > 0) and ((lon > 0) or (lon < 0)):
        url = url + '?lat=' + str(lat) + '&lon=' + str(lon)
    response = urlopen(url)
    result = json.loads(response.read())
    return result
   
def iss_people():
# Call web service to obtain details of people on board ISS
    result = web_service_interface('http://api.open-notify.org/astros.json')

# Print number of people in space to console+
    print('------------------------------------')
    print('People in Space: ', result['number'])
    print('------------------------------------')

# Loop through details of each person on board ISS and print to console
    people = result['people']
    for p in people:
        print("Name:  " + p['name'] + "\nCraft: " + p['craft'] + "\n")

    print('------------------------------------')

def iss_location():
# Call web service to obtain details of ISS location
    result = web_service_interface('http://api.open-notify.org/iss-now.json')

# Store response in variables - turtle requires float for x,y coords
    location = result['iss_position']
    lat = float(location['latitude'])
    lon = float(location['longitude'])
    timestamp = result['timestamp']

# Print results to console
    print('ISS current location')
    print('------------------------------------')
    print('Latitude: ', lat)
    print('Longitude: ', lon)

# Open a turtle screen, set size to 720 x 360
# Set world coordinates and BG pic to map provided by NASA
    screen = turtle.Screen()
    screen.setup(720, 360)
    screen.setworldcoordinates(-180, -90, 180, 90)
    screen.bgpic('images/map.gif')

# Set image for turtle to show ISS loc
    screen.register_shape('images/iss.gif')
    iss = turtle.Turtle()
    iss.shape('images/iss.gif')
    iss.setheading(90)

# Move turtle to current ISS coords
    iss.penup()
    iss.goto(lon, lat)
    iss_overhead()
    turtle.mainloop()

    
def iss_overhead():
    lat = 51.0305632
    lon = -3.1091860000000224

    location = turtle.Turtle()
    location.penup()
    location.color('yellow')
    location.goto(lon,lat)
    location.dot(5)
    location.hideturtle()

    result = web_service_interface('http://api.open-notify.org/iss-pass.json', lat, lon)
    over = time.ctime(result['response'][1]['risetime'])
    style = ('Arial', 6, 'bold')
    location.write(over, font=style)

    print('Next over Craig Lea: ' + over)


iss_people()
iss_location()
