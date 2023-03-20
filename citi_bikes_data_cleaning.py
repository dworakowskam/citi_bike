# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 09:02:28 2023

@author: MD
"""

import pandas as pd

ver0 = 'C:/MD/Dokumenty/python/data_analysis/citi_bikes/New York Citi Bikes_Raw Data - NYCitiBikes.csv'
ver1 = 'C:/MD/Dokumenty/python/data_analysis/citi_bikes/New York Citi Bikes_Raw Data - NYCitiBikes1.csv'

def read_file(filepath):
    return pd.read_csv(filepath)

def save_file(data_frame, filepath, index=False):
    return data_frame.to_csv(filepath, index=index)



if __name__ == "__main__":
    
    
    df = read_file(ver0)
    
    # Removing duplicates
    df.duplicated().sum()
    df = df.drop_duplicates()
    
    # Handling missing data
    df.isnull().sum()
    df = df.dropna(subset=['End Station Name'])
        
    save_file(df, ver1)
    
