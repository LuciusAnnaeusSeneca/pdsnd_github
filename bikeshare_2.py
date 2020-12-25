import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITIES = ['chicago', 'new york city', 'washington']
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june','all']
DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all' ]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    while True:
        city = input('Enter Chicago, New York City, or Washington:').lower()
        if city in CITIES:
            break
        else:
            print ('You typed something wrong! Please type in the correct city name!')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Enter a month between January and June or type all to review everything:').lower()
        if month in MONTHS:
            break
        else:
            print ('You typed something wrong! Please type in the correct month!')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Enter a weekday to review or type all to review everything:').lower()
        if day in DAYS:
            break
        else:
            print ('You typed something wrong! Please type in the correct day!')


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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()
    print('The most common month is: ', common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()
    print('The most common day of week is: ', common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('The most common hour to start to travel is: ', common_hour)
    #display how long the trip takes
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("Most popular end stattion:", popular_end_station)

    # display most frequent combination of start station and end station trip
    df['Start End Combo'] = df['Start Station'] + ' and ' + df['End Station']
    print('Most common route:')
    print(df['Start End Combo'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time in hours:', (total_travel_time / 60) / 60)

    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print('Average travel time in minutes:', avg_travel_time / 60)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    user_types = df['User Type'].value_counts()
    print('Number of users:\n', user_types)

    # display counts of gender
    if 'Gender' in df:
         gender = df['Gender'].value_counts()
         print("Counts by gender:\n",gender)
    else:
        print("Gender data not available!")


    # display earliest, most recent, and most common year of birth
    if 'Birth_Year' in df:
        earliest_year = df['Birth_Year'].min()
        print("Earliest birth year is: ",earliest_year)
        recent_year = df['Birth_Year'].max()
        print('Most recent birth year is: ',recent_year)
        common_year = df['Birth Year'].mode()[0]
        print('The most common birth year is: ',common_year)
    else:
        print("Birth year data not available!")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_data = input('\nWould you like to see 5 lines of raw data?\nPlease enter yes or no: \n').lower()
        if raw_data in ('yes', 'y'):
            i = 0
            while True:
                print(df.iloc[i:i+5])
                i += 5
                show_next = input('Would you like to see the next 5 lines of raw data? Please enter yes or no: \n').lower()
                if show_next not in ('yes', 'y'):
                    break
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
