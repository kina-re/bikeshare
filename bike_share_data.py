# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 12:28:58 2018

@author: krina
"""

import time
from datetime import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

month_data = ['January', 'February', 'March', 'April', 'May', 'June']

week_data = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    #while loop for input validation
    #choose city from available three options     
    your_city = True
    
    while your_city:       
       city = input("Please choose city from chicago, new york city and washington: ").lower()
      
       if city not in (CITY_DATA):
           print("Please choose from the options given to you")
       else:
           your_city = False
       
    #choose month from available six options 
    your_month = True
     
    while your_month:
     
       month = input("Please enter the month(January, February, March, April, May, June) or type 'all': ").title()
       
       if month not in (month_data) and not 'All':
           print("Please choose from the options given to you")
       else:
           your_month = False      
           
       #choose day of a week from available seven options 
       your_day = True
       
       while your_day:
           
           day = input("Please enter the day(Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday) or type 'all': ").title()
           
           if day not in (week_data) and not 'All':
               print("Please choose from the options given to you")           
           else:
              your_day = False         
               
      
    #just a separator with forty dashes
    print('-'*40)
    
    return city, month, day

 
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # Choose the csv file, date parser is to easily parsed dates in string formats   
    df = pd.read_csv(CITY_DATA[city], parse_dates = ['Start Time', 'End Time'])
    
    # Replace NaN values with zero
    df.fillna(0)
    
    #Choose to see first five rows of all available columns for your chosen city
    while True:
          five_rows = input("Enter 'yes' or 'no' to get first five rows of all columns: ").lower()
          print('')
          if five_rows == "yes":
              print(df.head())
              print('')
              break
          elif five_rows == "no":
              break
          else:
              print("please enter 'yes' or 'no'")
              False        
            
    # Get datetime column from starttime
    df['Start Time'] = pd.to_datetime(df['Start Time'])    
    
    # Extract month , day and hour from start time
    df['month'] = df['Start Time'].dt.month
    df['month'] = pd.to_datetime(df['Start Time']).dt.strftime('%B')
    df['day']=pd.to_datetime(df['Start Time']).dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    
    # Most common month
    common_month = df['month'].mode()
    print("Most common month when no filter is applied: ", common_month)  
                
    # Filter by month if 'all' is not an imput
    if month != 'All':
         
        #filter by month to create a new dataframe
        try:
            df = df[df['month'] == month]
        except KeyError as error:
            print("Error occured")            
            
    # Filter by day to create a new data frame
    if day != 'All':
        
        # Filter by day to create a new dataframe
        try:
            df = df[df['day'] == day]
        except KeyError as error:
            print("Error occured")

    return df


def station_stats(df):
    
    # Most commonly used start station
    try:        
        comm_start_station = df['Start Station'].mode().to_string(index = False)        
        print("Most commonly used Start Station is:", comm_start_station)        
        print()
                
    except KeyError as error:        
        print("error occured")
        
        
    # Most commonly used end station
    try:        
        comm_end_station = df['End Station'].mode().to_string(index = False)        
        print("Most commonly used End Station is:", comm_end_station)
        print('')        
        
    except KeyError as error:        
        print("error occured")
        
        
    # Most commonly used start and end station    
    try:        
        df['trip'] = df['Start Station'].str.cat(df['End Station'], sep = ' -> ')        
        to_fro = df['trip'].mode()        
        print("Most commonly used start to stop stations are:", to_fro)  
                
    except KeyError as error:        
        print("error occured")
        
    return df  

   
def trip_duration_stats(df):
    
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common start hour
    common_start_hour = df['hour'].mode()
    print("Most common start hour is: ", common_start_hour)  
    
    # total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time is: ", total_travel_time)
    
    # Avarage travel time
    avg_travel_time = df['Trip Duration'].mean()
    print("Avarage travel time is:", avg_travel_time)    

    #Duration of process
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    return df

    
def user_stats(df): 
    
    """
    Displays count of user types, count of gender
    
    Displays erliest, most recent and most common year of birth
    
    """
    # Count user types
    user_type = df['User Type'].value_counts()
    print("User types are: \n",user_type)
    print('')
    
    # Counts of Gender
    try:        
        gender_count = df['Gender'].value_counts()
        print("The gender counts are:\n",gender_count)
        print('')
        
    
    except:
        print("No data for Gender exist or error occured")
    
    #Earliest, most recent and most common year of birth
    try:        
        earl_birth = df['Birth Year'].min()
        print("The earliest birth year is:",earl_birth)
        print('')
        
        recent_birth = df['Birth Year'].max()    
        print("Most recent birth year is:",recent_birth)
        print('')
        
        common_birth = df['Birth Year'].mode()
        print("Most common birth year is:",common_birth)
        print('')
    
    except:
        print("No data for birth exist or error occured")
  
    return df
 
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)        
        station_stats(df)
        trip_duration_stats(df)        
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()    
        
      
    
    
              
    