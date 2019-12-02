import pandas
import numpy
import pymysql
import os
import platform
import time
from tabulate import tabulate
import datetime

conn = pymysql.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    passwd = '1234',
    database = 'ticket'
)

c = conn.cursor()

def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def create_booking():
    try:
        clear()
        display = pandas.read_sql("select * from flight;", conn)
        print(tabulate(display, headers=['Flight No','Airlines','Departure Destination','Departure Time','Arrival Time','Seats Available','Price'], tablefmt='fancy_grid', showindex=False))
        f_no = int(input("Enetr the flight no: "))
        gst = lambda y: ((y/100) * 18)
        booked = pandas.DataFrame(columns=['Flight No','Airlines','Departure Destination','Departure Time','Arrival Destination','Arrival Time','Price','Tax','Total Price'])
        price = int(display.loc[f_no - 1]['price'])
        tax = round(gst(price), 2)
        total_price = tax + price
        date = datetime.datetime.now()
        flight = display.loc[f_no - 1]['airlines']
        dic = {
            'Flight No': display.loc[f_no - 1]['flight_id'],
            'Airlines': display.loc[f_no - 1]['airlines'],
            'Departure Destination': display.loc[f_no - 1]['departure_destination'],
            'Departure Time': display.loc[f_no - 1]['departure_time'],
            'Arrival Destination': display.loc[f_no - 1]['arrival_destination'],
            'Arrival Time': display.loc[f_no - 1]['arrival_time'],
            'Price': price,
            'Tax': tax,
            'Total Price': total_price
        }
        booked = booked.append(dic, ignore_index=True, sort=False)
        print(tabulate(booked, headers='keys', tablefmt='fancy_grid', showindex=False))
        confirm = input("Do you want to confirm your booking?[y/n] ")
        if confirm == 'y':
            clear()
            name = input("Please enter your name: ")
            email = input("Please enter your email: ")
            phone = input("Please enter your phone number: ")
            c.execute(f"""insert into booking values (Null, "{f_no}", "{flight}", "{name}", "{email}", "{phone}","{price}", "{tax}", "{total_price}", "{date}");""")
            conn.commit()
        else:
            pass

    except KeyboardInterrupt:
        pass


def view_booking():
    booking = pandas.read_sql("select flight_id, flight_name, pas_name, pas_email, pas_phone, booking_date , price, tax, total_price from booking;", conn)
    print(tabulate(booking, showindex=False, tablefmt="psql", headers=['Flight ID', 'Airlines','Passenger Name','Passenger email','Passenger Phone','Date of Booking','Price', 'Tax', 'Total Price']))
    input()

def main():
    try:
        while True:
            print("""Options:
            1. View Bookings
            2. Book Flight
            3. Exit""")
            opt = int(input("> "))
            if opt == 1:
                view_booking()
                clear()
            elif opt == 2:
                create_booking()
                clear()
            else:
                break
    
    except KeyboardInterrupt:
        pass

main()