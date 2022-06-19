import math
from tkinter import *
from tkinter import ttk
import random
import pandas
import json

BUTTON_TEXT = ("Birch std", 12, 'italic')

weather_list = ['Normal', 'Cold', 'Hot', 'Extreme Heat', 'Extreme Cold', 'Light Wind',
                'Strong Wind', 'Light Rain', 'Light Snow', 'Heavy Rain', 'Heavy Snow']

class DmTimer:
    """An easy to use GUI based D&D time tracker."""

    def __init__(self):
        # ------------------------------------- Lists ----------------------------------------------
        self.days = ['Starday', 'Sunday', 'Moonday', 'Godsday', 'Waterday', 'Earthday', 'Freeday']
        self.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                       'August', 'September', 'October', 'November', 'December']
        self.seasons = ['Winter', 'Spring', 'Summer', 'Autumn']
        self.modes_of_travel = ['Walking', 'Galley', 'Keelboat', 'Longship', 'Rowboat',
                                'Sailing Ship', 'Warship', 'Draft Horse', 'Riding Horse', 'Griffon', 'Pegasus']
        self.travel_speed = ['Slow', 'Medium', 'Fast']

        # Read saved data and set up variables needed for methods:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
        self.hour = int(data['hour'])
        self.min = int(data['minute'])
        self.date_counter = int(data['date_counter'])
        self.month_counter = int(data['month_counter'])
        self.season_counter = int(data['season_counter'])
        self.day = self.days[self.date_counter % 7]
        self.season = self.seasons[self.season_counter]
        self.month = self.months[self.month_counter % 12]
        self.round_count = 0
        self.reg_distance = 0
        data = pandas.read_csv("D&D 5e Travel Speeds - Sheet1.csv")
        self.travel_dict = data.to_dict('records')
        print(self.travel_dict)
        self.travel_choice = {}
        self.current_weather = []
        self.update_weather()

        # ------------------------- GUI Initialization -----------------------------
        self.window = Tk()
        self.window.title("DM Clock")
        self.window.config(height=600, width=800)

        # ------------------------------- Canvas ------------------------------------
        self.canvas = Canvas(width=600, height=200)
        image = PhotoImage(file="sun_and_cloud.png")
        self.canvas.create_image(300, 100, image=image)
        self.time_text = self.canvas.create_text(220, 70, text=f"{self.hour}:{self.min}",
                                                 fill="black", font=("Birch std", 24, 'italic'))
        self.weather_text = self.canvas.create_text(325, 165,
                                                    text=f'{self.current_weather[0]}, {self.current_weather[1]}',
                                                    fill="black", font=BUTTON_TEXT)
        self.date_text = self.canvas.create_text(475, 60, text=f'Day: {self.day}\nDate: {self.date_counter}\n'
                                                               f'Month: {self.month}\nSeason: {self.season}',
                                                 fill='black', font=BUTTON_TEXT)
        self.canvas.grid(column=0, columnspan=4, row=1)

        # ------------------------------- Buttons ------------------------------------
        self.weather_button = Button()
        self.weather_button.config(width=20, text='Weather Generator', font=BUTTON_TEXT, command=self.weather_generator)
        self.weather_button.grid(column=0, row=2, padx=10, pady=10)

        self.s_rest_button = Button()
        self.s_rest_button.config(width=20, text='Short Rest', font=BUTTON_TEXT, command=self.short_rest)
        self.s_rest_button.grid(column=1, columnspan=2, row=2, padx=10, pady=10)

        self.l_rest_button = Button()
        self.l_rest_button.config(width=20, text='Long Rest', font=BUTTON_TEXT, command=self.long_rest)
        self.l_rest_button.grid(column=3, row=2, padx=10, pady=10)

        self.time_input_button = Button()
        self.time_input_button.config(width=10, text='Busy', font=BUTTON_TEXT, command=self.busy)
        self.time_input_button.grid(column=3, row=3, padx=10, pady=10)

        self.travel_button = Button()
        self.travel_button.config(width=20, text='Calculate Travel Time',
                                  font=BUTTON_TEXT, command=self.gui_travel_timer)
        self.travel_button.grid(column=1, columnspan=2, row=5, padx=10, pady=10)

        self.set_time_button = Button()
        self.set_time_button.config(width=20, text='Set Time', font=BUTTON_TEXT, command=self.set_time)
        self.set_time_button.grid(column=3, row=6, pady=10, padx=10)

        self.save_button = Button()
        self.save_button.config(text='Save', command=self.update_data)
        self.save_button.grid(column=1, row=7)

        # ------------------------------- Labels ------------------------------------
        self.title = Label()
        self.title.config(text='DM Time and Travel Clock', fg='Black', font=("Birch std", 24, 'italic'))
        self.title.grid(column=1, columnspan=2, row=0)

        self.busy_label = Label()
        self.busy_label.config(text='Time Busy:', fg='Black', font=BUTTON_TEXT)
        self.busy_label.grid(column=0, row=3, pady=10, padx=10)

        self.travel_label = Label()
        self.travel_label.config(text='Travel Details:', fg='Black', font=BUTTON_TEXT)
        self.travel_label.grid(column=0, row=4, padx=10, pady=20)

        self.set_time_label = Label()
        self.set_time_label.config(text='Set the time:', fg='black', font=BUTTON_TEXT)
        self.set_time_label.grid(column=0, row=6, pady=10, padx=10)

        # ------------------------------- Entries ------------------------------------
        self.busy_entry = Entry()
        self.busy_entry.config(width=30, highlightthickness=0)
        self.busy_entry.grid(column=1, columnspan=2, row=3)
        self.busy_entry.insert(END, 'Enter in minutes: e.g. 120')

        self.distance_entry = Entry()
        self.distance_entry.config(width=20, highlightthickness=0)
        self.distance_entry.grid(column=2, row=4)
        self.distance_entry.insert(END, '--km')

        self.set_time_hour_entry = Entry()
        self.set_time_hour_entry.config(width=20, highlightthickness=0)
        self.set_time_hour_entry.grid(column=1, row=6)

        self.set_time_minute_entry = Entry()
        self.set_time_minute_entry.config(width=20, highlightthickness=0)
        self.set_time_minute_entry.grid(column=2, row=6)

        # ------------------------------- Comboboxes ------------------------------------
        self.vehicle_choice = ttk.Combobox(self.window, values=self.modes_of_travel, width=20)
        self.vehicle_choice.grid(column=1, row=4)

        self.speed_choice = ttk.Combobox(self.window, values=self.travel_speed, width=20)
        self.speed_choice.grid(column=3, row=4)

        # Test button - Use for testing Commands for bugs.
        self.test_button = Button()
        self.test_button.config(text='Test', command=self.test)
        self.test_button.grid(column=0, row=7)

        # Main Loop
        self.update_timer()
        self.window.mainloop()
        self.update_data()

    # ------------------------------- Methods ------------------------------------

    def test(self):
        """Used with the test button
        Here to be used for any future methods."""
        # self.hour += 1
        # self.update_timer()

    def gui_travel_timer(self):
        """
        Method that calculates time taken travelling using the following:

                   Distance - Speed of travel - Mode of travel

        Triggers the update_timer method upon completion
        """
        self.reg_distance = int(self.distance_entry.get())
        vehicle = self.vehicle_choice.get()
        travel_rate = self.speed_choice.get()
        speed = 0
        for travel_type in self.travel_dict:
            if travel_type['Mode of Transport'] == vehicle:
                speed = int(travel_type[travel_rate])
        time_taken = self.reg_distance / (speed / 60)
        added_hours = math.floor(time_taken / 60)
        print(added_hours)
        added_mins = int(time_taken % 60)
        print(added_mins)
        self.min += added_mins
        self.hour += added_hours
        self.update_timer()
        self.canvas.itemconfig(self.time_text, text=f'{self.time}')

    def update_timer(self):
        """Method for updating the clock, day, month and season values"""
        # Change 60 mins to 1 hour and reset the mins to 0
        if self.min >= 60:
            self.hour += 1
            self.min -= 60
        # Some of the code can add many more hours - Have to keep deducting until below
        # 24 hours - adding to the date counter for each day over.
        while self.hour >= 24:
            self.date_counter += 1
            # All the months have 28 days - Therefore when the limit is reached, the date is reset and
            # The month counter is increased.
            if self.date_counter > 28:
                self.month_counter += 1
                self.date_counter -= 28
                # Make sure that the month counter stays below 12.
                while self.month_counter > 12:
                    self.month_counter -= 12
            self.hour -= 24
        # Update the date values
        self.update_day()
        self.update_month()
        self.update_season()
        self.update_date()
        # Generate the time to be updated on the Canvas
        self.count = ((self.hour * 60) + self.min)
        self.clock_min = self.count % 60
        if self.clock_min < 10:
            self.clock_min = f"0{self.clock_min}"
        self.time = f"{math.floor(self.count / 60)}:{self.clock_min}"
        print(self.time)

    def round_counter(self):
        """Keeps track of rounds and adds minutes when needed."""
        self.round_count += 1
        if self.round_count >= 10:
            self.min += 1
            self.round_count = 0
            self.update_timer()

    def short_rest(self):
        """Receives number of hours and minutes of short rest and then updates the timer."""
        self.hour += 1
        self.update_timer()
        self.canvas.itemconfig(self.time_text, text=f'{self.time}')

    def long_rest(self):
        """Receives number of hours and minutes of short rest and then updates the timer."""
        self.hour += 7
        self.update_timer()
        self.canvas.itemconfig(self.time_text, text=f'{self.time}')
        self.weather_generator()

    def busy(self):
        """Receives number of hours and minutes of short rest and then updates the timer."""
        total_added = int(self.busy_entry.get())
        added_hours = int(math.floor(total_added / 60))
        added_mins = int(total_added % 60)
        self.hour += added_hours
        self.min += added_mins
        self.update_timer()
        self.canvas.itemconfig(self.time_text, text=f'{self.time}')

    def set_time(self):
        """This Method allows the user to manually set the time and date
        *****Future update***** Allow the user to input a manual date."""
        self.hour = int(self.set_time_hour_entry.get())
        self.min = int(self.set_time_minute_entry.get())
        self.update_timer()
        self.canvas.itemconfig(self.time_text, text=f'{self.time}')

    def weather_generator(self):
        """Method to generate weather and update it on the canvas."""
        self.update_weather()
        self.canvas.itemconfig(self.weather_text, text=f'{self.current_weather[0]}, {self.current_weather[1]}')

    def update_weather(self):
        """
        This Method will return the current weather of the game like so:
        Relative Temperature - Wind Strength - Precipitation
        """
        self.current_weather.clear()
        # Temperature generation
        temp_chance = random.randint(1, 20)
        if 14 < temp_chance < 18:
            if self.season == "Winter":
                self.current_weather.append("Extreme Cold")
            else:
                self.current_weather.append("Cold")
        elif temp_chance > 17:
            if self.season == "Summer":
                self.current_weather.append("Extreme Heat")
            else:
                self.current_weather.append("Hot")
        else:
            self.current_weather.append("Normal Temperature")
        # Wind force generation
        wind_chance = random.randint(1, 20)
        if 12 < wind_chance < 18:
            self.current_weather.append("Light Wind")
        elif wind_chance > 17:
            self.current_weather.append("Strong Wind")
        else:
            self.current_weather.append("No wind")
        # Precipitation generation (snow if winter - rain if not)
        precipitation_chance = random.randint(1, 20)
        if 12 < precipitation_chance < 18:
            if self.season == "Winter":
                self.current_weather.append("Light Snow")
            else:
                self.current_weather.append("Light Rain")
        elif precipitation_chance > 17:
            if self.season == "Winter":
                self.current_weather.append("Heavy Snow")
            else:
                self.current_weather.append("Heavy Rain")
        else:
            self.current_weather.append("No Precipitation")
        print(self.current_weather)

    def update_data(self):
        """Method to save the data in the clock_data.txt file."""
        data_store = [str(self.hour), str(self.min), str(self.date_counter), str(self.month_counter),
                str(self.season_counter)]
        new_data = {
            'hour': self.hour,
            'minute': self.min,
            'date_counter': self.date_counter,
            'month_counter': self.month_counter,
            'season_counter': self.season_counter,
        }
        with open("data.json", "w") as data_file:
            # Replace the json file with the new data.
            json.dump(new_data, data_file, indent=4)


    def update_day(self):
        self.day = self.days[self.date_counter % 7]

    def update_month(self):
        self.month = self.months[self.month_counter % 12]

    def update_date(self):
        self.canvas.itemconfig(self.date_text, text=f'Day: {self.day}\nDate: {self.date_counter}\n'
                                                    f'Month: {self.month}\nSeason: {self.season}')

    def update_season(self):
        """Determines the season based on the current month."""
        if self.month_counter < 2 or self.month_counter == 11:
            self.season_counter = 0
        elif 5 > self.month_counter >= 2:
            self.season_counter = 1
        elif 8 > self.month_counter >= 5:
            self.season_counter = 2
        elif 11 > self.month_counter >= 8:
            self.season_counter = 3
        elif self.month_counter > 11:
            self.season_counter = 0
        self.season = self.seasons[self.season_counter]


DmTimer()
