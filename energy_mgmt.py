import streamlit as st
import time
import pandas as pd
import numpy as np
import plotly.express as px

# References: 
# 1) https://docs.streamlit.io/library
# 2) https://gist.github.com/rxaviers/7360908
# 3) https://youtu.be/_Um12_OlGgw?si=LUJMz9CNax6aSSkC
# 4) https://youtu.be/vIQQR_yq-8I?si=AbOO57_xpN9XsrmE



CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


allowed_city = ['Chicago', 'New York City', 'Washington']

allowed_buildings = [None, 'all', 'January', 'February', 'March', 'April', 'May', 'June']

allowed_months = [None, 'all', 'January', 'February', 'March', 'April', 'May', 'June']


allowed_days = ['all', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']



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
    df = pd.read_csv(CITY_DATA[city.lower()])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['month']=df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        df = df[df['month'] == month.title()]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    st.write('-'*40)
    st.write('#### Calculating The Most Frequent Times of Travel...')
    start_time = time.time()
    col1, col2, col3 = st.columns(3)
    # display the most common month
    col1.metric("Most common month", df['month'].mode()[0])

    # display the most common day of week
    col2.metric("Most common day of week", df['day_of_week'].mode()[0])

    # display the most common start hour
    col3.metric("Most common start hour", f"{df['Start Time'].dt.hour.mode()[0]}:00")
 

    st.write("\nThis took {} seconds.".format(round(time.time() - start_time, 3)))
    st.write('-'*40)
    

def minutes_format(minutes):
  """Converts minutes to days, hours, and minutes.

  Args:
    minutes: The number of minutes.

  Returns:
    A tuple of (days, hours, minutes).
  """

  days = minutes // (60 * 24)
  hours = (minutes % (60 * 24)) // 60
  minutes = minutes % 60

  return int(days), int(hours), int(minutes)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    st.write('#### Calculating The Most Popular Stations and Trip...')
    start_time = time.time()
    
    tab1, tab2, tab3 = st.tabs(["Start station", "End Station", "Combination of Stations"])

    with tab1:
        # display most commonly used start station
        st.metric("Most commonly used Start Station", df['Start Station'].mode()[0])

    with tab2:
        # display most commonly used end station
        st.metric("Most commonly used End Station:", df['End Station'].mode()[0])

    with tab3:
        # display most frequent combination of start station and end station trip
        df['combination_station'] = df['Start Station'] + " + " + df['End Station']
        st.markdown(f"###### Most Frequent combination of Start - End station:") 
        st.markdown(f"#### {df['combination_station'].mode()[0]}")
        
    st.write("\nThis took {} seconds.".format(round(time.time() - start_time, 3)))
    st.write('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    st.write('#### Calculating Trip Duration...')
    start_time = time.time()
    # display total travel time
    total_time= df['Trip Duration'].sum()
    day,hour,minute = minutes_format(total_time)

    
    tab1, tab2 =st.tabs(['Travel Time', "Date"])
    #Travel Time Metric
    with tab1:
        st.metric("Total travel time",  f"{day} day(s), {hour} hr(s) and {minute} min(s)")
    # display mean travel time
        mean_travel_time = df['Trip Duration'].mean()
        day2,hour2,minute2 = minutes_format(mean_travel_time)

        st.metric("The mean travel time", f"{day2} day(s), {hour2} hr(s) and {minute2} min(s)")

    #Date Metric    
    with tab2:
        col1, col2 = st.columns(2)
        col1.metric("From", str(df['Start Time'].dt.date.min()) )
        col2.metric("To", str(df['End Time'].dt.date.max()))
        

    st.write("\nThis took {} seconds.".format(round(time.time() - start_time, 3)))
    st.write('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    st.write('#### Calculating User Stats...')
    start_time = time.time()

    tab1, tab2 = st.tabs(["Birth Analysis", "User & Gender Count"])
    with tab1:
        col1, col2, col3 = st.columns(3)
        if ('Birth Year' in df.columns):
            # Display earliest, most recent, and most common year of birth
            col1.metric("Earliest year of birth", int(df['Birth Year'].min()))
            col2.metric("Most recent year of birth", int(df['Birth Year'].max()))
            col3.metric("Most common year of birth", int(df['Birth Year'].mode()[0]))

    with tab2:
        col4, col5 = st.columns(2)
        # Display counts of user types
        col4.write(df['User Type'].value_counts())
        if ('Gender' in df.columns):
            # Display counts of gender
            col5.write(df['Gender'].value_counts())


    st.write("\nThis took {} seconds.".format(round(time.time() - start_time, 3)))
    st.write('-'*40)

def plotter_for_heatmap():
    '''
    Generates a plotly bar chart for the top 10 count of unique values in a column of a dataframe

    Arguments:
    str(column_name): Type in a string of a column name as it is diplayed on the dataframe
    str(dataframe): Type in a dataframe object you wish to analyze
    '''
    #result = dataframe[column_name].value_counts()[:10]

    #plot_obj =px.bar(result, x=result.index, 
                    #y=column_name, 
                    #title=f"Top 10 {column_name}",
                    #text= column_name,
                    #labels={'index':column_name, 'Start Station': f'Count of {column_name}' })

        # 1. Load the CSV file.
    dataframe = pd.read_csv("Energy_usage_x052a_2024.csv")

    # 2. (Optional) Parse the date column if needed.
    #    Adjust "Date" to whatever your date column is called, and specify the correct format.
    # df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")

    #drop the three first columns
    dataframe.drop(dataframe.columns[:3], axis=1, inplace=True)

    # 3. Set the date column as the DataFrame index, so rows become individual dates.
    dataframe.set_index("Date", inplace=True)

    # 4. Sort the half-hour columns in chronological order (optional but helpful).
    #    If your columns are strings like "0:30", "1:00", "1:30", etc., 
    #    we can parse them as timedeltas to sort properly.
    #    If “24:00:00” causes a parsing error, you might rename it to "24:00" or similar.
    #df = df[sorted(df.columns, key=lambda x: pd.to_timedelta(x))]

    # 5. Create the heatmap using px.imshow (wide-format data).
    plot_obj = px.imshow(
        dataframe[334:],
        color_continuous_scale="RdYlGn_r",  # Red = higher usage, Green = lower usage
        labels={"color": "Usage (kWh)"},
        aspect="auto"
    )

    plot_obj.update_layout(
        title="Half-Hourly Energy Usage Heatmap in Cranfield University for January 2025",
        xaxis_title="Time of Day",
        yaxis_title="Date"
    )
    #plot_obj.update_traces(texttemplate='%{text:.2s}', textfont='outside')
    plot_obj.update_traces(
    xgap=1.5,  # gap between columns
    ygap=1.5,  # gap between rows
    hoverongaps=False  # optional, to disable hover on the gap areas)
    )
    st.plotly_chart(plot_obj, use_container_width=True)

#This initilizes the streamlit's session_state dictionary in the format 'stage' : 0
if 'stage' not in st.session_state:
    st.session_state.stage = 0
def set_stage(i):
    st.session_state.stage = i

def main():
    st.markdown('# Hello! Let\'s explore Cranfield\'s database!:smiley:')
    st.markdown("###### :warning: NOTE: You must enter the correct period. Else, the program will not run :warning:")

    city_message = "Choose the building number: (Chicago, New York City or Washington): "
    
    # get user input for city (chicago, new york city, washington) before proceeding to the next stage of the app
    city = st.text_input(city_message, on_change=set_stage, args=[1]).lower()
   
    if city.title() not in allowed_city:
        set_stage(0)

    
    if st.session_state.stage >= 1:
        month_message = "Choose your month you want to analyze: January, February, March, April, May, June or all: "

        # get user input for month (all, january, february, ... , june)
        month =st.selectbox(month_message, np.array(allowed_months), on_change=set_stage, args=[2])
        if month is None:
            set_stage(1)

    if st.session_state.stage >= 2:
        day_message = "Choose your day you want to analyze: \n monday, tuesday, wednesday, thursday, friday, saturday, sunday or all:"

        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = st.selectbox(day_message, np.array(allowed_days))
        
        # gets user input for number of rows of the dataframe to be displayed 
        rows = st.number_input("How manys rows of the dataframe do you wish to see? ", min_value=0, max_value=100, step=5)
        
        st.button("Calculate", on_click=set_stage, args=[3])

    if st.session_state.stage >= 3:
        # Progress Bar that loads the the three tabs
        my_bar = st.progress(0)

        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1)
        st.success("Done")
        # End of progress bar

        #Loading the dataframe
        df = load_data(city, month, day)
        
        tab1, tab2, tab3 = st.tabs(["**Descriptive Statistics**", "**View DataFrame**", "**Charts**:chart_with_downwards_trend:"])

        #This tab contains the descriptive statistics
        with tab1:
            st.markdown("## Click the expander to see! :point_down:")
            with st.expander("### Click to view Descriptive Statistics"):

                time_stats(df)
                station_stats(df)
                trip_duration_stats(df)
                user_stats(df)
        
        #This tab contains the dataframe if the user wishes to view it
        with tab2:

            if rows != 0:
                df2 = pd.read_csv("Energy_usage_x052a_2024.csv")
                st.write(df2.head(rows))
            else:
                st.write('_Select number of rows to view from above_')

        #This tab contains the necessary charts of the descriptive statistics
        with tab3:
            plotter_for_heatmap()
            #visual_value = st.selectbox("Choose a column to see the count of its unique values: ", [None, 'Start Station', 'End Station', 'combination_station'])
        
            #f visual_value is not None:
                #plotter(visual_value, df)
        
        # Click button to restart the whole program
        st.button("Restart:o:", on_click=set_stage, args=[0])
        
            

if __name__ == "__main__":
	main()
