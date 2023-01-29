import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = [
      'monday',
      'tuesday',
      'wednesday',
      'thursday',
      'friday',
      'saturday',
      'sunday'
]
responses = ['yes','no']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city_chosen = input("Would you like to see the data of Chicago, New York or Washington?"+'\n')
        if city_chosen.lower() in CITY_DATA:
            city = city_chosen.lower()
            break
        else:
            print("Please enter a valid city")

    # get user input for month (all, january, february, ... , june)
    filtered_by = input("Would you like to filter your data by month, day, both or none?"+'\n')
    while True:
        if filtered_by.lower() == 'month' or filtered_by.lower() == 'both' :
            month = input("Which month? January, Feburary, March, April, May, June?"+'\n')
            if month.lower() in months:
                month = month.lower()
                break
            else:
                print("Month doesn't exist")
        else:
            month = 'all'
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        if filtered_by.lower() == 'day' or filtered_by.lower() == 'both' :
            day = input("Which day? Monday, Tuesday , Wednesday, Thursday, Friday, Saturday, Sunday?"+'\n')
            if day.lower() in days:
                day = day.lower()
                break
            else:
                print("day doesn't exist")
        else:
            day = 'all'
            break



        if filtered_by.lower() == 'none':
            month = day ='all'
            break





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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour']= df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month']== month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframed
        df = df[df['day_of_week'] == day.title()]


    return df





def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    # display the most common month
    # we used the calendar module to get the month name as dt.day_name didn't work on this version of python
    most_common_month = df['month'].mode()[0]
    print("The most common month:{} ({}) ".format(most_common_month, calendar.month_name[most_common_month]))
    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print("The most common day of week: " , most_common_day_of_week )

    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print("The most common hour: " , most_common_hour )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("The most common start station: " , most_common_start_station)
    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("The most common start station: " , most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_combination = (df['Start Station'] + ' ' +df['End Station'] ).mode()[0]
    print("The most frequent combination of start station and end station: " , most_combination)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_minutes = total_travel_time.round()/60
    total_hours = total_travel_time.round()/3600
    print("The total travel time is:  {} seconds , {} minutes , {} hours ".format(total_travel_time.round(),total_minutes.round(),total_hours.round()))
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_minutes = total_travel_time.round()/60
    mean_hours = total_travel_time.round()/3600
    print("The mean travel time is: {} seconds , {} minutes , {} hours ".format(mean_travel_time.round(),mean_minutes.round(),mean_hours.round()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""


    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print("The count of each user type:" +'\n' , user_type_counts)
    # Display counts of gender
    # this condition is here as 'washington.csv' doesn't hava a gender column
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("The count of each gender:" +'\n' , gender_counts)

    # Display earliest, most recent, and most common year of birth
    # this condition is here as 'washington.csv' doesn't hava a birth year column
    if 'Birth Year' in df.columns:
        earliest_birth_year =  df['Birth Year'].min()
        print("The earliest birth year: {} ".format(int(earliest_birth_year)))
        recent_birth_year =  df['Birth Year'].max()
        print("The most recent birth year: {} ".format(int(recent_birth_year)))
        common_birth_year =  df['Birth Year'].mode()[0]
        print("The most common birth year: {} ".format(int(common_birth_year)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_more_data(df):
    """Show and display data and ask the user whether he wants to see more data or not upon his input"""
    
    print('\nShowing User More Data...\n')

    d=0
    choice = input("Do you want to see more data? yes or no?" + '\n')
    if choice.lower() not in responses:
        print("Please enter yes or no")
        choice = input("Do you want to see more data? yes or no?" + '\n')
    elif choice.lower() == 'yes':
        while d+5 <= df.shape[0]-1:
            print(df.iloc[d:d+5,:])
            d+=5
            choice = input("Do you want to see more data? yes or no?" + '\n')
            if choice.lower() == 'no':
                break







def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        #This function used to show more raw data
        show_more_data(df) 


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
	main()
