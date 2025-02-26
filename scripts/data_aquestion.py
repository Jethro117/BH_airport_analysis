import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime
import time

def collect_flight_data(day, flight_direction):
    '''
    This function scrapes data from the Bahrain Airport website and returns it as a table.

    Args:
        day (str): 'TD' for Today or 'TM' for Tomorrow
        flight_direction (str): 'arrivals' or 'departures'

    Returns:
        Pandas DataFrame with 8 columns
    '''
    url = f"https://www.bahrainairport.bh/flight-{flight_direction}?date={day}"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    
    time_lst = []
    destination_lst = []
    airways_lst = []
    gate_lst = []
    status_lst = []
    flight_lst = []

    flights = soup.find_all("div", {"class": f"flight-table-list row dv{flight_direction[:-1].title()}List"}) #ArrivalList

    for flight in flights:
        try:
            airways_lst.append(flight.find('img')["alt"])
        except:
            airways_lst.append(pd.NA)
        
        status_lst.append(flight.find('div', class_="col col-flight-status").text.strip())
        flight_lst.append(flight.find('div', class_="col col-flight-no").text.strip())
        destination_lst.append(flight.find('div', class_="col col-flight-origin").text.strip())
        time_lst.append(flight.find('div', class_="col col-flight-time").text.strip())
        gate_lst.append(flight.find('div', class_="col col-gate").text.strip())

    flights_data = {
        'destination': destination_lst,
        'flight_number': flight_lst,
        'airline': airways_lst,
        'gate': gate_lst,
        'status': status_lst,
        'time': time_lst
    }
    df = pd.DataFrame(flights_data)
    
    if day == 'TD':
        date = datetime.date.today()
    elif day == 'TM':
        date = datetime.date.today() + datetime.timedelta(days=1)
        
    df['date'] = date
    df['direction'] = flight_direction
    
    return df

def collect_arrival_dep():

    tables = []
    directions =['arrivals', 'departures']
    days = ['TD' , 'TM']
    
    for direction in directions:
        for day in days:
            tables.append(collect_flight_data(day,direction))
            time.sleep(10)
    df = pd.concat(tables)
    return df

def save_data(df):
    today = datetime.date.today()
    path= f'all_flights_data_(today).csv'.replace('-','_')
    df.to.csv(path)
        
df = collect_arrival_dep()
save_data(df)




