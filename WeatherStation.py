from tkinter import *
import requests
import base64
from urllib.request import urlopen
import tkinter.messagebox


class WeatherStation:

    def __init__(self, master):
        self.email = 'your_email_here'
        self.key = "your_key_here"
        self.imageDir = "http://openweathermap.org/img/w/"
        self.imageExt = ".png"
        # self.email = email
        # self.key = key


# initialisation
root = Tk()
root.title("WeatherStation")
b = WeatherStation(root)


def get_weather(city, api_key):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID={}'.format(city, api_key)
    print(url)

    try:
        r = requests.get(url)
        if r.status_code != 200:
            problem = r.json()
            tkinter.messagebox.showerror(problem['cod'], problem['message'])
            return None
        else:
            return r.json()

    except:
        print('Exception found')
        tkinter.messagebox.showerror("Problem", "An exception have been caught")


def get_formatted(weather):
    details = []
    main_weather = weather['weather'][0]
    main = main_weather['main']
    details.append(main)
    main_desc = main_weather['description']
    details.append(main_desc)
    main_temp = weather['main']['temp']
    temp_val = int(main_temp - 273.15)
    details.append(temp_val)
    city = weather['name']
    details.append(city)
    country = weather['sys']['country']
    details.append(country)
    wind = weather['wind']['speed']
    details.append(wind)
    icon = weather['weather'][0]['icon']
    get_weather_image(icon)
    print(details)
    return details


# label
label_city = Label(root, text="City: ")
val_temp_desc = Label(root, font=("Verdana", 16))
label_overcast = Label(root, text="Overcast", font=("Verdana", 24))

# values
val_temp_info = Label(root)
val_temp = Label(root)
val_city = Label(root)
val_country = Label(root)
label_wind = Label(root, text='Wind')
val_wind = Label(root)

# entry
entry_city = Entry(root)
entry_city.focus()

# images
icon = PhotoImage()
labelIcon = Label(root, image=icon)


def start_process(city):
    data = get_weather(city, b.key)
    if data == None:
        return None
    else:
        formatted = get_formatted(data)
        val_temp_desc['text'] = formatted[0]
        val_temp_info['text'] = formatted[1]
        val_temp['text'] = formatted[2]
        val_city['text'] = formatted[3]
        val_country['text'] = formatted[4]
        val_wind['text'] = formatted[5]  # This item was not added to the grid, please try yourself and share your comments
        return formatted


def get_weather_image(image):
    path = b.imageDir + image + b.imageExt
    image_byte = urlopen(path).read()
    image_b64 = base64.encodestring(image_byte)
    icon['data'] = image_b64


# button
btn_run = Button(root, text="Run", width=5, command=lambda: start_process(entry_city.get()))

# grid
label_city.grid(row=0, pady=5, sticky=W)  # City:
entry_city.grid(row=0, column=1, sticky=W)  # Entry for city
btn_run.grid(row=0, column=2, padx=5, pady=20)  # Run Button

label_overcast.grid(row=1, columnspan=3)  # Overcast label
val_city.grid(row=2, columnspan=3)  # City
val_country.grid(row=3, columnspan=3)  # Country
labelIcon.grid(row=4, columnspan=3)  # Image pulled from the weather api
val_temp.grid(row=5,  columnspan=3)  # Temperature in degrees
val_temp_desc.grid(row=6, columnspan=3)  # Description
val_temp_info.grid(row=7, columnspan=3, pady=5)  # More info

root.mainloop()
