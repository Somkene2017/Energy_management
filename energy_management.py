import streamlit as st
import time
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# References: 
# 1) https://docs.streamlit.io/library
# 2) https://gist.github.com/rxaviers/7360908
# 3) https://youtu.be/_Um12_OlGgw?si=LUJMz9CNax6aSSkC
# 4) https://youtu.be/vIQQR_yq-8I?si=AbOO57_xpN9XsrmE
# 5) <a href="https://www.flaticon.com/free-icons/water" title="water icons">Water icons created by Freepik - Flaticon</a>
# 6) <a href="https://www.flaticon.com/free-icons/clean-energy" title="clean energy icons">Clean energy icons created by Flat Icons - Flaticon</a>
# 7) <a href="https://www.flaticon.com/free-icons/carbon" title="carbon icons">Carbon icons created by juicy_fish - Flaticon</a>
# 8) Zelvion Energy (Energy Entrepreneurship -- Cranfield University)

st.set_page_config(page_title="Cloudberry Energy Dashboard", page_icon="cloudberry_logo_2.png",layout="wide")


#BUILDING_DATA = { 'XO52A': 'Energy_usage_x052a_2024.csv',}
BUILDING_DATA =pd.read_csv("Energy_usage_cranfield_campus_buildings_2024.csv")
WATER_DATA =pd.read_csv("Water_usage_cranfield_campus_buildings_2024.csv")

building_data_2 = BUILDING_DATA[BUILDING_DATA["site_name"] == "Campus Energy"]
#Total of all Utilities (i.e., Energy, Water and CO2)
total_annual_energy_consumption = int(building_data_2[building_data_2.columns[4:]].sum(axis=1).sum())
total_annual_water_consumption = int(WATER_DATA[WATER_DATA.columns[4:]].sum(axis=1).sum())

# st.metric("Total Annual Energy Consumption (KWh)", f"{total_annual_energy_consumption:,}")
# st.metric("Total Annual Water Consumption (m\u00b3)", f"{total_annual_water_consumption:,}")



#allowed_city = ['Chicago', 'New York City', 'Washington']

allowed_buildings = BUILDING_DATA['site_name'].unique().tolist()
allowed_buildings.insert(0, None)
allowed_months = [None, 'all', 'January', 'February', 'March', 'April', 'May', 'June']


allowed_days = [None, 'all', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']



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
    #df = BUILDING_DATA.copy()

    # Load Water data
    water = WATER_DATA[WATER_DATA["site_name"] == building]
    water['Date'] = pd.to_datetime(water['Date'])

    water['month']=water['Date'].dt.month_name()
    water['day_of_week'] = water['Date'].dt.day_name()

    if month != 'all':
        water = water[water['month'] == month.title()]
    if day != 'all':
        water = water[water['day_of_week'] == day.title()]

    #load building data
    if building != None:
        df = BUILDING_DATA[BUILDING_DATA["site_name"] == building]

    df['Date'] = pd.to_datetime(df['Date'])
   #df['End Time'] = pd.to_datetime(df['End Time'])

    df['month']=df['Date'].dt.month_name()
    df['day_of_week'] = df['Date'].dt.day_name()

    if month != 'all':
        df = df[df['month'] == month.title()]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df, water

# Function to create a donut gauge
def create_gauge(title, building_annual, total_annual, color, unit, utility):
    progress = (building_annual / total_annual) * 100
    progress = min(progress, 100)  # Ensure it doesn't exceed 100%

    fig = go.Figure()

    # Add main progress arc
    fig.add_trace(go.Pie(
        values=[progress, 100 - progress],
        labels=["Progress", ""],
        hole=0.7,
        marker=dict(colors=[color, "lightgray"]),
        textinfo="none",
        sort=False
    ))

    # Add percentage text in the center 
    fig.add_annotation(
        text=f"<b>{round(progress,2)}%</b>",
        x=0.5, y=0.5,
        #font=dict(size=28, color="white"),
        font=dict(size=28),
        showarrow=False
    )

    # Layout settings
    fig.update_layout(
        showlegend=False,
        width=300, height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        #paper_bgcolor="black",
        #plot_bgcolor="black"
    )

    # Display in Streamlit
    with st.container():
        st.markdown(f"<h4 style='text-align: center; color: white;'>{title}</h4>", unsafe_allow_html=True)
        col4, col5 = st.columns(2)
        col4.plotly_chart(fig)
        with st.container():
            col5.metric(f"Annual {utility} Cons. ({unit})", f"{building_annual:,}")
            col5.metric(f"Tot. Annual {utility} Cons. ({unit})", f"{total_annual:,}")


def Load_Total_Utility_stats(df):
    """Displays statistics on the most popular stations and trip."""

    usage_cols = df.columns.drop(["site_name", "Date", "month", "day_of_week","site_code", "meter_reference", "site_code"])
    # 5. Sum usage values across each row to get daily total energy usage
    #df['month'] = df['Date'].dt.month_name()
    df["daily_total"] = df[usage_cols].sum(axis=1)
    # 7. Group by month and sum daily totals to get monthly energy usage
    daily_totals = df.groupby("Date")["daily_total"].sum().reset_index()
    return daily_totals

def format_ghg_intensity(value):
    """Formats GHG emission intensity with appropriate unit and CO₂ subscript."""
    co2e = "CO\u2082e"  # Unicode for CO₂e (₂ = U+2082)
    
    if value >= 1:
        return f"{value:,} kg {co2e}/kWh"
    else:
        return f"{value * 1000:,} g {co2e}/kWh"
    
def Total_Energy_stats(energy, water):
    st.write('#### Calculating Utility Usage Statistics...')
    start_time = time.time()

    energy_usage = Load_Total_Utility_stats(energy)
    water_usage = Load_Total_Utility_stats(water)

    col1, col2, col3 = st.columns(3)
    col1.image("clean.png")
    col2.image("water.png")
    col3.image("CO2.png")

    energy_cons = int(energy_usage.daily_total.sum())
    water_cons = int(water_usage.daily_total.sum())

    col4,col5,col6 = st.columns(3)
    col4.metric("Annual Energy Consumption (KWh)", f"{energy_cons:,}")
    col5.metric("Annual Water Consumption (m\u00b3)", f"{water_cons:,}")
    #col6.metric("Annual CO2 Emissions (kgCO\u2082e/kWh)", f"{format_ghg_intensity(0.7)}")
    col6.metric("Annual CO2 Emissions (gCO\u2082e/kWh)", f"{700}")

    st.write("\nThis took {} seconds.".format(round(time.time() - start_time, 3)))
    st.write('-'*40)


def Maximum_Energy_stats(df,utility,unit):
    """Displays statistics on the most popular stations and trip."""

    st.write(f'#### Calculating Maximum {utility} Usage Statistics...')
    start_time = time.time()
    
    col1, col2, col3 = st.columns(3)
    df2 = df.drop(df.columns[:3], axis=1)

    df3 = df2.drop(df2.columns[-3:], axis=1)
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

    # display Maximum Usage
    col1.metric(f"Maximum {utility} usage", f"{max_usage} {unit}")

    # display Time of occurence of Maximum Usage
    col2.metric("Occurred on:", f"{max_date}")

    # display Time of occurence of Maximum Usage
    col3.metric("Time:", f"{max_time}")
        
    st.write("\nThis took {} seconds.".format(round(time.time() - start_time, 3)))
    st.write('-'*40)



def plotter_for_heatmap(df,month, building_name, utility, unit):
    '''
    Generates a plotly bar chart for the top 10 count of unique values in a column of a dataframe

    Arguments:
    str(column_name): Type in a string of a column name as it is diplayed on the dataframe
    str(dataframe): Type in a dataframe object you wish to analyze
    '''

        # 1. Load the CSV file.
    df2 = df.drop(df.columns[:3], axis=1)

    df3 = df2.drop(df2.columns[-2:], axis=1)
    # 3. Set the date column as the index.
    #    Replace "Date" with the actual name of your date column if different.
    df4 = df3.set_index("Date")    

    # 5. Create the heatmap using px.imshow (wide-format data).
    plot_obj = px.imshow(
        df4,
        color_continuous_scale="RdYlGn_r",  # Red = higher usage, Green = lower usage
        labels={"color": f"Usage ({unit})"},
        aspect="auto"
    )

    plot_obj.update_layout(
        title=f"{building_name} Half-Hourly {utility} Heatmap in Cranfield University for {month} 2024",
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
    
def total_energy_bar_chart_per_month(df, building_name, utility, unit):
    
    # 4. Group by month and sum daily totals to get monthly energy usage
    monthly_totals = df.groupby("month")["daily_total"].sum().reset_index()
    
    # 5. Create a month order dictionary for proper sorting
    month_order = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    
    # 6. Sort the dataframe by month order
    monthly_totals['month_num'] = monthly_totals['month'].map(month_order)
    monthly_totals = monthly_totals.sort_values('month_num').drop('month_num', axis=1)
    
    # 7. Create a bar chart using Plotly Express
    fig = px.bar(
        monthly_totals,
        x="month",
        y="daily_total",
        labels={
            "month": "Month",
            "daily_total": f"Total {utility} ({unit})"
        },
        title=f"Total {utility} per Month for {building_name} in 2024"
    )
    
    # 8. Update layout for better readability
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False,
        height=500,
        width=800,
        margin=dict(t=50, b=100)  # Adjust margins for better label visibility
    )
    
    # 9. Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    return fig  # Return the figure object for additional customization if needed

def total_energy_line_chart_per_month(df_site, building_name, day, month, utility, unit):


    # 7. Group by month and sum daily totals to get monthly energy usage
    daily_totals = df_site.groupby("Date")["daily_total"].sum().reset_index()

    # 8. Create a bar chart using Plotly Express
    if day != "all":
        fig = px.line(
            daily_totals,
            x="Date",
            y="daily_total",
            labels={"month": "Month", "daily_total": "Total Energy (kWh)"},
            title=f"{building_name} Profile Energy Data for all {day}s in {month}, 2024"
        )
    else:
        fig = px.line(
            daily_totals,
            x="Date",
            y="daily_total",
            labels={"month": "Month", "daily_total": f"Total {utility} ({unit})"},
            title=f"{building_name} Profile {utility} Data for {month}, 2024"
        )

    fig.update_layout(xaxis_tickangle=-45)    
    # Rotate x-axis labels for better readability
    st.plotly_chart(fig, use_container_width=True)


def decison_maker(building):
    # Room data
    data = [
        {"name": f"{building} Room1", "temp": 15, "co2": 434, "humidity": 23, "controls": ["Heating (ASHP/GSHP)", "Lightbulb 1", "Lightbulb 2"]},
        {"name": f"{building} Room2", "temp": 24, "co2": 232, "humidity": 26, "controls": ["Heating (ASHP/GSHP)", "Lightbulb 1"]},
        {"name": f"{building} Room3", "temp": 23, "co2": 143, "humidity": 30, "controls": ["Heating (ASHP/GSHP)", "Lightbulb 1", "Lightbulb 2"]}
    ]

    st.title("Real Time (AI-Driven) Control")
    st.text_input("Search Room", placeholder="Search Room")

    for room in data:
        with st.container():
            st.subheader(f"{room['name']}")
            st.checkbox("Saving Mode", key=f"saving_mode_{room['name']}")
            st.write(f"Temperature {room['temp']}°C | CO2 Concentration {room['co2']} ppm | Humidity {room['humidity']}%")
            
            for control in room["controls"]:
                col1, col2 = st.columns([1, 0.1])
                with col1:
                    st.checkbox(control, key=f"{control}_{room['name']}")
                with col2:
                    st.text("🔒")

#This initilizes the streamlit's session_state dictionary in the format 'stage' : 0
if 'stage' not in st.session_state:
    st.session_state.stage = 0
def set_stage(i):
    st.session_state.stage = i

def main():
    #st.markdown(dark_mode_css, unsafe_allow_html=True)
    # Now insert some more in the container
    col_prompt, col_metrics, col_AI = st.columns(3)
    with st.container():
        with col_prompt.container():
            col_prompt.image("cloudberry_logo.png", caption=f"Cloudberry...All-in-One, Hassle-Free, Cost-Saving Energy Optimization​")
            col_prompt.markdown('### Hello! Let\'s explore Cranfield\'s Energy Consumption database!:smiley:')
            col_prompt.markdown("###### :warning: NOTE: Your required analysis will be based on the building you select. :warning:")

            building_message = "Choose the building number: (Baroness Young Hall, X Building 052A Vincent,X Data Centre [C049], etc): "
            
            # get user input for building (chicago, new york city, washington) before proceeding to the next stage of the app
            building = col_prompt.selectbox(building_message, np.array(allowed_buildings), on_change=set_stage, args=[1])
        
            if building == None:
                set_stage(0)

            
            if st.session_state.stage >= 1:
                month_message = "Choose your month you want to analyze: January, February, March, April, May, June or all: "

                # get user input for month (all, january, february, ... , june)
                month =col_prompt.selectbox(month_message, np.array(allowed_months), on_change=set_stage, args=[2])
                if month is None:
                    set_stage(1)

            if st.session_state.stage >= 2:
                day_message = "Choose your day you want to analyze: \n monday, tuesday, wednesday, thursday, friday, saturday, sunday or all:"

                # get user input for day of week (all, monday, tuesday, ... sunday)
                day = col_prompt.selectbox(day_message, np.array(allowed_days), on_change=set_stage, args=[3])
                if day is None:
                    set_stage(2)
                
                # gets user input for number of rows of the dataframe to be displayed 
                rows = col_prompt.number_input("How manys rows of the data table do you wish to see? ", min_value=0, max_value=100, step=5)
                # Progress Bar that loads the the three tabs
                my_bar = col_prompt.progress(0)

                for percent_complete in range(100):
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1)
                col_prompt.success("Done")
                # End of progress bar

          
                #st.button("Calculate", on_click=set_stage, args=[3])            
            #col_prompt.write("1")

    if st.session_state.stage >= 3:
        #Loading the dataframe
        df, water = load_data(building, month, day)      
        if rows != 0:
        #df = pd.read_csv("Energy_usage_x052a_2024.csv")
        #df2 = df.drop(df.columns[-2:], axis=1)
            col_prompt.markdown('##### Energy Table')
            col_prompt.write(df.head(rows))
        else:
            col_prompt.write('_Select number of rows to view from above_')          
        with col_metrics.container():
            #Loading the dataframe
            #decison_maker(building)
            Total_Energy_stats(df, water)

            x = int(df['daily_total'].sum())
            y = int(water['daily_total'].sum())
            donut_metrics = {
                "Electricity Consumption":         {
                    "building_annual": x,
                    "total_annual": total_annual_energy_consumption,
                    "color": "#FFC000",  # Yellow
                    "unit": "kWh",
                    "utility": "Energy"
                },
                "Water Consumption": {
                    "building_annual": y,
                    "total_annual": total_annual_water_consumption,
                    "color": "#28A745",  # Green
                    "unit": "m\u00b3",
                    "utility": "Water"
                }
            }

            utility_metrics = {
            "Electricity Consumption": {
                "utility": "Energy",
                "unit": "kWh"
            },
            "Water Consumption": {
                "utility": "Water",
                "unit": "m\u00b3"
                }
            } 
            
            #Total_Energy_stats(df,water)
            Maximum_Energy_stats(df, **utility_metrics["Electricity Consumption"])
            #col_energy, col_water = st.columns(2)
            #with col_energy:
            create_gauge("Electricity Metrics", **donut_metrics["Electricity Consumption"])
            #with col_water:
            create_gauge("Water Metrics", **donut_metrics["Water Consumption"])
            #Maximum_Energy_stats(water, **utility_metrics["Water Consumption"])    
            # col_metrics.write("2")


        with col_AI.container():
            decison_maker(building)
            if rows != 0:
                #df = pd.read_csv("Energy_usage_x052a_2024.csv")
                #df2 = df.drop(df.columns[-2:], axis=1)
                col_AI.markdown('##### Water Usage Table')
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                col_AI.write(water.head(rows))
        
            else:
                st.write('_Select number of rows to view from above_')                   
            



        col_map, col_data_table, col_chart = st.columns(3)
        with st.container():
            with col_map.container():
                col_map.image("Cranfield_University_campus_map-1.png", caption="Cranfield University Map")


            with col_data_table.container():
                total_energy_bar_chart_per_month(df, building, **utility_metrics["Electricity Consumption"])
                total_energy_bar_chart_per_month(water, building, **utility_metrics["Water Consumption"])
    


            with col_chart.container():
                plotter_for_heatmap(df, month, building, **utility_metrics["Electricity Consumption"])
                plotter_for_heatmap(water, month, building, **utility_metrics["Water Consumption"])


            
        col_line_chart_1, col_line_chart_2 = st.columns(2)
        with col_line_chart_1:
            total_energy_line_chart_per_month(df, building,day, month, **utility_metrics["Electricity Consumption"])
        with col_line_chart_2:
            total_energy_line_chart_per_month(water, building,day, month, **utility_metrics["Water Consumption"]) 


            #visual_value = st.selectbox("Choose a column to see the count of its unique values: ", [None, 'Start Station', 'End Station', 'combination_station'])
        
            #f visual_value is not None:
                #plotter(visual_value, df)
        
        # Click button to restart the whole program
        st.button("Restart:o:", on_click=set_stage, args=[0])
        
            

if __name__ == "__main__":
	main()
