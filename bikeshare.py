from calendar import month
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

GENDER = False

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
        city = input("What city you would like to see it's data? (chicago, new york city, washington) ").lower()
        if city in ['chicago','new york city','washington']:
            break
        else:
            print('you entered a wrong city...')

    # get user to filter by day or month or both
    while True:
        filt = input("Filter by (day, month, both, none) ").lower()
        if filt in ['day','month','both','none']:
            break
        else:
            print('you entered a wrong type of filter...')

    # to prevent reference before assignment error
    day = 'all'
    month = 'all'
    
    if filt != 'none':
        if (filt == 'month' or filt == 'both'):
    
            # get user input for month (all, january, february, ... , june)
            while True:
                month = input("Which month?: (all, january, february, ... , june) ").lower()
                if month in ['all', 'january', 'february', 'march', 'april', 'june']:
                    break
                else:
                    print('you entered a wrong month...')
    
        if (filt == 'day' or filt == 'both'):
            # get user input for day of week (all, monday, tuesday, ... sunday)
            while True:
                day = input("Which day? (all, saturday , sunday , monday, ..., friday) ").lower()
                if day in ['all','saturday','sunday','monday','tuesday','wednesday','thrusday','friday']:
                    break
                else:
                    print('you entered a wrong day...')

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
    global GENDER
    
    # Reading the csv file 
    df = pd.read_csv(CITY_DATA[city])

    # set gender to True as washington has no gender column  
    if city != 'washington':
        GENDER = True

    # convert Start Time to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    ### Filtering by month
    # Add new column with filtered month names
    df['month'] = df['Start Time'].dt.month_name()

    # filter by month to create new dataframe
    if month != 'all':
         df = df[df['month'] == month.title()]

   
    ### Filtering by day
    # Add new column with filtered day names
    df['day'] = df['Start Time'].dt.day_name()

    # filter by day to create new dataframe
    if day != 'all':
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # check if df is empty or not 
    if df.empty:
        
        print('There is no available data')
        
    else:
        
        # display the most common month
        most_comm_month = df['month'].mode()[0]
        print('The most common month for travelling:',most_comm_month)
        print('')

        # display the most common day of week
        most_comm_day = df['day'].mode()[0]
        print('The most common day for travelling:',most_comm_day)
        print('')

        ### display the most common start hour
        # create start hour column
        df['start_hour'] = df['Start Time'].dt.hour

        most_comm_hour = df['start_hour'].mode()[0]
        print('The most common start hours for travelling:',most_comm_hour)
        print('')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # check if df is empty or not 
    if df.empty:
        
        print('There is no available data')
        
    else:
    
        # display most commonly used start station
        most_used_start = df['Start Station'].mode()[0]
        print('The most commonly used start station for travelling is:',most_used_start)
        print('')

        # display most commonly used end station
        most_used_end = df['End Station'].mode()[0]
        print('The most commonly used end station for travelling is:',most_used_end)
        print('')

        # display most frequent combination of start station and end station trip
        most_used_comb = (df['Start Station'] + ' and ' + df['End Station']).mode()[0]
        print('The most commonly used start and end station combined are:',most_used_comb)
        print('')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # check if df is empty or not 
    if df.empty:
        
        print('There is no available data')
        
    else:
        
        # display total travel time
        total_travel_time = df['Trip Duration'].sum()
        print('Total trip time is:')
        calc_time(total_travel_time)
        print('')


        # display mean travel time
        mean_travel_time = df['Trip Duration'].mean()
        print('Average trip duration is:')
        calc_time(mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)   


def user_stats(df):
    """Displays statistics on bikeshare users."""
    
    global GENDER

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # check if df is empty or not 
    if df.empty:
        
        print('There is no available data')
        
    else:
        # Display counts of user types
        user_types = df['User Type'].value_counts()
        print('Calculating number of users:')
        print(user_types)
        print('')


        if GENDER == True:
            # Display counts of gender
            user_genders = df['Gender'].value_counts()
            print('Calculating count of Gender:')
            print(user_genders)
            print('')

            ### Display earliest, most recent, and most common year of birth

            # drop rows with NAN values
            new_df = df.copy(deep = True)
            new_df.dropna(subset=['Birth Year'], axis = 0, inplace = True)

            #sort dataframe by Birth Year
            new_df.sort_values('Birth Year',ascending = True ,inplace = True)


            #earliest year of birth
            earliest_year = new_df['Birth Year'].iloc[0]
            print('Earliest year of birth is: ' + str(int(earliest_year)))
            print('')

            #most recent year of birth
            recent_year = new_df['Birth Year'].iloc[-1]
            print('Most recent year of birth is: ' + str(int(recent_year)))
            print('')

            #most common year of birth
            common_year = new_df['Birth Year'].mode()[0]
            print('Most common year of birth is: ' + str(int(common_year)))
            print('')
    
    #reset gender indicator
    GENDER = False
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def calc_time(seconds):
    '''Convert seconds into (hours, minutes, seconds) and display them'''
    
    seconds = seconds % (24*3600)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    print(int(hours),'hours,', int(minutes), 'minutes,', int(seconds), 'seconds.')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
