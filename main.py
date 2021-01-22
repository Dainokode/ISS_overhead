import requests
from datetime import datetime
import smtplib
import time


MY_LAT = "your latitude"
MY_LNG = "your longitude"


def is_overhead():
    # Get ISS position
    request_iss = requests.get("http://api.open-notify.org/iss-now.json")
    request_iss.raise_for_status()
    data_1 = request_iss.json()


    latitude = float(data_1["iss_position"]["latitude"])
    longitude = float(data_1["iss_position"]["longitude"])
    iss_position = (latitude, longitude)


    if MY_LAT+5 <= iss_position[0] >= MY_LAT-5 and MY_LNG+5 <= iss_position[1] >= MY_LNG-5:
        return True



def is_sunset():
    # Get sunrise and sunset based on your location
    parameters = {
        "lat": 20.300321,
        "lng": -5.844790,
        "formatted": 0
    }


    request_sunset = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    request_sunset.raise_for_status()
    data_2 = request_sunset.json()


    sunrise = int(data_2["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data_2["results"]["sunset"].split("T")[1].split(":")[0])


    time_now = datetime.now().hour
    

    if time_now >= sunset:
        return True


def send_email():
    my_email = "your email"
    password = "your password"
    receiver = "email receiver"
    message = "The ISS is currently over your head!"

    if is_overhead and is_sunset:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            fmt = 'From: {}\r\nTo: {}\r\nSubject: {}\r\n{}'
            connection.sendmail(
                my_email,
                receiver,
                fmt.format(my_email, receiver, "Look Up!", message).encode('utf-8')
            )


while True:
    time.sleep(6000)
    send_email()