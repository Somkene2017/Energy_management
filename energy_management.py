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



#BUILDING_DATA = { 'XO52A': 'Energy_usage_x052a_2024.csv',}
BUILDING_DATA =pd.read_csv("Energy_usage_cranfield_campus_buildings_2024.csv")

#allowed_city = ['Chicago', 'New York City', 'Washington']

allowed_buildings = [None, 'all', "Airfield solar PV array",
    "Campus building PVs",
    "Campus Energy",
    "Total campus electricity",
    "Total Cranfield Campus PV",
    "X 63 & 52 IT Servers",
    "X AIRC Building",
    "X B91 compressor house",
    "X Baroness Young 1",
    "X Baroness Young 2",
    "X Baroness Young 3",
    "X Baroness Young 4",
    "X Baroness Young 5",
    "X Baroness Young block 1-5",
    "X Building 003",
    "X Building 019",
    "X Building 026",
    "X Building 029",
    "X Building 032",
    "X Building 037",
    "X Building 038",
    "X Building 039",
    "X Building 040",
    "X Building 041",
    "X Building 042",
    "X Building 043",
    "X Building 043A",
    "X Building 044",
    "X Building 045",
    "X Building 046",
    "X Building 050",
    "X Building 052 Whittle",
    "X Building 052A Vincent",
    "X Building 053",
    "X Building 054 Hudson",
    "X Building 061",
    "X Building 062",
    "X Building 063",
    "X Building 070",
    "X Building 083",
    "X Building 083 IMEC",
    "X Building 088",
    "X Building 090",
    "X Building 108",
    "X Building 111",
    "X Building 115",
    "X Building 122",
    "X Building 240",
    "X Building 30",
    "X Building 33",
    "X Chilver 2",
    "X Chilver 3",
    "X Conference Hotel",
    "X Conway House",
    "X Fedden Flats",
    "X Icing Tunnel",
    "X Lanchester 11",
    "X Lanchester 12",
    "X Lanchester 13",
    "X Lanchester 14",
    "X Lanchester 15",
    "X Lanchester 16",
    "X Lanchester 4",
    "X Lanchester 5",
    "X Lanchester 6",
    "X Lanchester 7",
    "X Lanchester 8",
    "X Lanchester 9",
    "X Lanchester Hall",
    "X Library",
    "X Martell House",
    "X Medway Court Unit 5 (BlockF)",
    "X Mitchell Hall",
    "X Stringfellow 1",
    "X Stringfellow 2",
    "X Stringfellow 3",
    "X Stringfellow 4",
    "X Stringfellow 5",
    "X Stringfellow Hall",
    "X VCO/Finance",
    "X085",
    "X146 FAAM",
    "XDARTeC",
    "XData centre (C049)",
    "XMedway Court Unit 3",
    "Xsharedhouses"
]

allowed_months = [None, 'all', 'January', 'February', 'March', 'April', 'May', 'June']


allowed_days = ['all', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']



def load_data(building, month, day):
    """
    Loads data for the specified building and filters by month and day if applicable.

    Args:
        (str) building - name of the building to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing building data filtered by month and day
    """
    df = BUILDING_DATA[BUILDING_DATA["site_name"] == building]

    df['Date'] = pd.to_datetime(df['Date'])
   #df['End Time'] = pd.to_datetime(df['End Time'])

    df['month']=df['Date'].dt.month_name()
    df['day_of_week'] = df['Date'].dt.day_name()

    if month != 'all':
        df = df[df['month'] == month.title()]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    st.write('-'*40)
    st.write('#### Calculating The Most Frequent Day of the month...')
    start_time = time.time()
    col1, col2, col3 = st.columns(3)
    # display the most common month
    col1.metric("Most common month", df['month'].mode()[0])

    # display the most common day of week
    col2.metric("Most common day of week", df['day_of_week'].mode()[0])

    # display the most common start hour
    col3.metric("Most common start hour", f"{df['Date'].dt.hour.mode()[0]}:00")
 

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


def Maximum_Energy_stats(df):
    """Displays statistics on the most popular stations and trip."""

    st.write('#### Calculating Energy Usage Statistics...')
    start_time = time.time()
    
    col1, col2, col3 = st.columns(3)
    df2 = df.drop(df.columns[:3], axis=1)

    df3 = df2.drop(df2.columns[-2:], axis=1)
    df3['Date'] = df3['Date'].dt.strftime("%Y-%m-%d")
    # Set the date column as the index.
    #    Replace "Date" with the actual name of your date column if different.
    df4 = df3.set_index("Date")


    # Convert the DataFrame from wide format (one row per date, columns for time intervals)
    #    into a long (stacked) Series with a MultiIndex (Date, Time).
    stacked = df4.stack()

    # 6. Find the maximum energy usage and its corresponding (Date, Time).
    max_usage = stacked.max()        # Maximum usage value
    max_idx = stacked.idxmax()         # MultiIndex tuple: (Date, Time)

    # 7. Unpack the tuple into the specific date and time.
    max_date, max_time = max_idx

    # 8. Print the results.
    #print(f"Maximum usage----->: {max_usage} kWh")
    #print(f"Occurred on: {max_date} at {max_time}")

    # display Maximum Usage
    col1.metric("Maximum usage", f"{max_usage} kWh")

    # display Time of occurence of Maximum Usage
    
    col2.metric("Occurred on:", f"{max_date}")


    col3.metric("Time:", f"{max_time}")
        
    st.write("\nThis took {} seconds.".format(round(time.time() - start_time, 3)))
    st.write('-'*40)



def plotter_for_heatmap(df,month):
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
    df2 = df.drop(df.columns[:3], axis=1)

    df3 = df2.drop(df2.columns[-2:], axis=1)
    # 3. Set the date column as the index.
    #    Replace "Date" with the actual name of your date column if different.
    df4 = df3.set_index("Date")    

    # 2. (Optional) Parse the date column if needed.
    #    Adjust "Date" to whatever your date column is called, and specify the correct format.
    # df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")

    # 4. Sort the half-hour columns in chronological order (optional but helpful).
    #    If your columns are strings like "0:30", "1:00", "1:30", etc., 
    #    we can parse them as timedeltas to sort properly.
    #    If “24:00:00” causes a parsing error, you might rename it to "24:00" or similar.
    #df = df[sorted(df.columns, key=lambda x: pd.to_timedelta(x))]

    # 5. Create the heatmap using px.imshow (wide-format data).
    plot_obj = px.imshow(
        df4,
        color_continuous_scale="RdYlGn_r",  # Red = higher usage, Green = lower usage
        labels={"color": "Usage (kWh)"},
        aspect="auto"
    )

    plot_obj.update_layout(
        title=f"Half-Hourly Energy Usage Heatmap in Cranfield University for {month} 2024",
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
    st.image("cloudberry_logo.png", caption="Cloudberry...All-in-One, Hassle-Free, Cost-Saving Energy Optimization​")
    st.markdown('# Hello! Let\'s explore Cranfield\'s database!:smiley:')
    st.markdown("###### :warning: NOTE: Your required analysis will be based on the building you select. :warning:")

    building_message = "Choose the building number: (Baroness Young Hall, X Building 052A Vincent,X Data Centre [C049], etc): "
    
    # get user input for building (chicago, new york city, washington) before proceeding to the next stage of the app
    building = st.selectbox(building_message, np.array(allowed_buildings), on_change=set_stage, args=[1])
   
    #if building.title() not in allowed_building:
       # set_stage(0)

    
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
        df = load_data(building, month, day)
        
        tab1, tab2, tab3 = st.tabs(["**Descriptive Statistics**", "**View DataFrame**", "**Charts**:chart_with_downwards_trend:"])

        #This tab contains the descriptive statistics
        with tab1:
            st.markdown("## Click the expander to see! :point_down:")
            with st.expander("### Click to view Descriptive Statistics"):

                time_stats(df)
                Maximum_Energy_stats(df)

        
        #This tab contains the dataframe if the user wishes to view it
        with tab2:

            if rows != 0:
                #df = pd.read_csv("Energy_usage_x052a_2024.csv")
                #df2 = df.drop(df.columns[-2:], axis=1)
                st.write(df.head(rows))
            else:
                st.write('_Select number of rows to view from above_')

        #This tab contains the necessary charts of the descriptive statistics
        with tab3:
            plotter_for_heatmap(df, month)
            #visual_value = st.selectbox("Choose a column to see the count of its unique values: ", [None, 'Start Station', 'End Station', 'combination_station'])
        
            #f visual_value is not None:
                #plotter(visual_value, df)
        
        # Click button to restart the whole program
        st.button("Restart:o:", on_click=set_stage, args=[0])
        
            

if __name__ == "__main__":
	main()
