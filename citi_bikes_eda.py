# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 19:56:55 2023

@author: MD
"""

import pandas as pd
import matplotlib.pyplot as plt
from citi_bikes_data_cleaning import save_file, read_file, ver1

ver2 = 'C:/MD/Dokumenty/python/data_analysis/citi_bikes/New York Citi Bikes_Raw Data - NYCitiBikes2.csv'


# QUESTIONS FOR ANSWERING:
# What are the most popular pick-up locations across the city for NY Citi Bike rental?
# How does the average trip duration vary across different age groups?
# Which age group rents the most bikes?
# How does bike rental vary across the two user groups (one-time users vs long-term subscribers) on different days of the week?
# Does user age impact the average bike trip duration?



if __name__ == "__main__":
    
    
    df = read_file(ver1)
       
    df["Trip_Duration_in_min"].dtypes
    # As trip_Duration_in_min is object type, we have to change it to numeric type.
    # Also we have "," which makes the conversion impossible, we have to remove them first.
    df = df.replace(',','', regex=True)
    df["Trip_Duration_in_min"] = pd.to_numeric(df["Trip_Duration_in_min"])
    trip_duration_in_min_description = df["Trip_Duration_in_min"].describe()
    trip_duration_in_min_sorted = df["Trip_Duration_in_min"].sort_values(ascending=False)
    # Max value seems unrealistic (6515 min is about 109 hours).
    # We are going to delete the heighest value as it seems to be the outlier
    df = df.drop(index=16342)
    trip_duration_in_min_description = df["Trip_Duration_in_min"].describe()
    trip_duration_in_min_mean_median = df["Trip_Duration_in_min"].median()
    
    df["Age"].dtypes
    age_description = df["Age"].describe()
    age_median = df["Age"].median()
    
       
    # What are the most popular pick-up locations across the city for NY Citi Bike rental?
    locations_sorted = (df.groupby(['Start Station Name']).agg(pick_ups_number=('Bike ID','count'))).pick_ups_number.sort_values(ascending=False)
    most_popular_locations = locations_sorted[:20]
    plt.figure(figsize=(15, 5))
    x = most_popular_locations.index.astype(str)[::-1]
    y = most_popular_locations[::-1]
    axes = plt.gca()
    axes.xaxis.grid()
    axes.set_axisbelow(True)
    plt.barh(x, y)
    plt.xlabel("Count", fontsize=12)
    plt.ylabel("Start station name", fontsize=12)
    plt.title("The most popular pick-up stations for NY Citi Bikes", fontsize=18)    
    plt.show()
    
    # How does the average trip duration varies across different age groups?
    age_groups_average_trip_duration = df.groupby(['Age Groups']).agg(average_trip_duration=('Trip_Duration_in_min','mean'))
    age_groups_average_trip_duration_sorted = age_groups_average_trip_duration.average_trip_duration.sort_values()
    plt.figure(figsize=(15, 5))
    x = age_groups_average_trip_duration_sorted.index.astype(str)
    y = age_groups_average_trip_duration_sorted[:]
    axes = plt.gca()
    axes.yaxis.grid()
    axes.set_axisbelow(True)
    plt.bar(x, y)
    plt.xlabel("Age group", fontsize=12)
    plt.ylabel("Average trip duration", fontsize=12)
    plt.title("Average trip duration (in min) per age group", fontsize=18)    
    plt.show()
    
    # Which age group rents the most bikes?
    age_groups_sorted = (df.groupby(['Age Groups']).agg(number_of_rentals=('Bike ID','count')))["number_of_rentals"].sort_values(ascending=False)
    plt.figure(figsize=(15, 5))
    x = age_groups_sorted.index.astype(str)
    y = age_groups_sorted[:]
    axes = plt.gca()
    axes.xaxis.grid()
    axes.set_axisbelow(True)
    plt.barh(x, y)
    plt.xlabel("Count of Bike ID", fontsize=12)
    plt.ylabel("Age group", fontsize=12)
    plt.title("Number of bikes rented across different age groups", fontsize=18)    
    plt.show()
    
    # How does bike rental vary across the two user groups (one-time users vs long-term subscribers) on different days of the week?
    weekday_user_type = pd.pivot_table(
        df, 
        index='Weekday', 
        columns='User Type', 
        values='Bike ID',
        aggfunc='count')
    plt.figure(figsize=(15, 5))
    x = weekday_user_type.index.astype(str)
    y1 = weekday_user_type["One-time user"]
    y2 = weekday_user_type["Subscriber"]
    axes = plt.gca()
    axes.yaxis.grid()
    axes.set_axisbelow(True)
    plt.stackplot(x,y1,y2, labels=["One-time users", "Subscribers"])
    plt.xlabel("Weekday", fontsize=12)
    plt.ylabel("Count of Bike ID", fontsize=12)
    plt.title("Number of bikes rented by one-time users and subscribers on different days of the week", fontsize=18)    
    plt.legend(loc="upper left")
    plt.show()
    
    # Does user age impact the average bike trip duration?
    plt.figure(figsize=(15, 5))
    x = df["Age"]
    y = df["Trip_Duration_in_min"]
    plt.scatter(x, y)
    plt.xlabel("Age", fontsize=12)
    plt.ylabel("Trip duration in minutes", fontsize=12)
    plt.title("Trip duration in minutes per age", fontsize=18)
    plt.show()
    
    
    save_file(df, ver2)
   
    

