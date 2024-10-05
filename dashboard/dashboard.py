import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Set the Seaborn style
sns.set(style='dark')

# Display the current working directory (for debugging)
st.write("Current working directory:", os.getcwd())

# Function to manipulate dataframe by hour
def byhour(df):
    hourly_rental = df.groupby(by='hour')['Total'].mean()
    return hourly_rental

# Function to manipulate dataframe by month
def bymonth(df):
    monthly_rental = df.groupby(by='month')['Total'].mean()
    return monthly_rental

# Load dataframes
day_df = pd.read_csv('day_modif_df.csv')
hour_df = pd.read_csv('hour_modif_df.csv')
season_df = pd.read_csv('melt_season_df.csv')
weather_df = pd.read_csv('melt_weathersit_df.csv')

# Convert date columns to datetime format
day_df['date_day'] = pd.to_datetime(day_df['date_day'])
hour_df['date_day'] = pd.to_datetime(hour_df['date_day'])

# Filter data by date range
min_date = hour_df["date_day"].min()
max_date = hour_df["date_day"].max()

with st.sidebar:
    # Add a logo to the sidebar
    st.image('https://raw.githubusercontent.com/fasya11/image/refs/heads/main/Desain%20tanpa%20judul.jpg', width=300)
    st.header('Bike Sharing')
    st.markdown("\n")

    st.markdown("""
    <div style="text-align: justify">
        Select a date
    </div>
    """, unsafe_allow_html=True)

    st.markdown("\n")

    # Create date input for range selection
    start_date, end_date = st.date_input(
        label='Range Time',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter main dataframe based on the selected date range
main_df = hour_df[(hour_df["date_day"] >= pd.Timestamp(start_date)) & 
                  (hour_df["date_day"] <= pd.Timestamp(end_date))]

# Prepare dataframes for hourly and monthly analysis
byhour_df = byhour(main_df)
bymonth_df = bymonth(hour_df)

# Header and introduction
st.header('Bike Sharing Analysis')
st.subheader('The Dashboard')
st.markdown("""
<div style="text-align: justify">
  This dashboard presents visual data related to bike usage based on time, month, season, and weather conditions. The information provides a comprehensive view of bike usage patterns, enabling users to understand trends, seasonal variations, and the impact of weather on bike activity.
</div>
""", unsafe_allow_html=True)

st.markdown("\n")

# Display daily bicycle users based on selected date range
date_range = f"{start_date} – {end_date}".replace("-", "/")
st.subheader(f'Daily Bicycle Users {date_range}')

# Show metrics for Casual, Registered, and Total users
col1, col2, col3 = st.columns(3)
with col1:
    casual_user = main_df['casual'].sum()
    st.metric("Casual Rental", value=casual_user)

with col2:
    registered_user = main_df['registered'].sum()
    st.metric("Registered Rental", value=registered_user)

with col3:
    total_user = main_df['Total'].sum()
    st.metric("Total Rental", value=total_user)

st.markdown("\n")

# Header for Data Analysis Section
st.header('Data Analysis')
analysis_option = st.selectbox('Choose Analysis',
                      ['Bike Rental and Revenue per Month',
                       'Bike Rental Distribution Per Hour',
                       'Bike Rental Distribution Per Season',
                       'Bike Rental Distribution Per Weather'])

# Monthly analysis
if analysis_option == 'Bike Rental and Revenue per Month':
    st.subheader('Average Monthly Bike Rental Users')

    # Plot monthly bike rental users
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.bar(bymonth_df.index, bymonth_df.values, color='#00E8FF')
    ax.set_xlabel('Month', fontsize=18, color='white')
    ax.set_ylabel('Average', fontsize=18, color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    
    # Set the plot and figure backgrounds
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#262730')

    # Display the plot
    st.pyplot(fig)

    with st.expander("See explanation"):
        st.write("""
        Based on data from 2011 to 2012, bicycle usage trends show an increase from the beginning of the year to the middle of the year, especially around June. From June to September, usage remains stable but begins to decline in October until the end of the year.
        """)

# Hourly analysis
elif analysis_option == 'Bike Rental Distribution Per Hour':
    st.subheader('Average Hourly Bicycle Riders')

    # Plot hourly bike rental users
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.bar(byhour_df.index, byhour_df.values, color='#00E8FF')
    ax.set_xlabel('Hour', fontsize=18, color='white')
    ax.set_ylabel('Average', fontsize=18, color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#262730')

    st.pyplot(fig)

    with st.expander("See explanation"):
        st.write("""
        On average, cyclists experience a notable increase at two specific times: during commuting hours around 8:00 am and again at 5:00 pm.
        """)

# Seasonal analysis
elif analysis_option == 'Bike Rental Distribution Per Season':
    st.subheader('Number of Bicycle Users by Season')

    # Plot bike rentals by season
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.bar(main_df['season'], main_df['Total'], color='#00E8FF')
    ax.set_xlabel('Season', fontsize=18, color='white')
    ax.set_ylabel('Number', fontsize=18, color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#262730')

    st.pyplot(fig)

    with st.expander("See explanation"):
        st.write("""
        The highest number of bicycle users occurred during summer, and the lowest occurred during winter, showing a right-skewed distribution.
        """)

# Weather analysis
elif analysis_option == 'Bike Rental Distribution Per Weather':
    st.subheader('Number of Bicycle Users by Weather')

    # Plot bike rentals by weather
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.bar(main_df['weathersit'], main_df['Total'], color='#00E8FF')
    ax.set_xlabel('Weather', fontsize=18, color='white')
    ax.set_ylabel('Number', fontsize=18, color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#262730')

    st.pyplot(fig)

    with st.expander("See explanation"):
        st.write("""
        The highest number of bicycle users occurred during clear weather, while the lowest occurred during heavy precipitation.
        """)

# Q&A Section
st.subheader('Question and Answer')
qa_option = st.selectbox('Choose a Question',
                      ['What is the correlation between weather changes and cyclists?',
                       'What patterns do cyclists make throughout the changing seasons?'])

# Answer for weather and cyclists
if qa_option == 'What is the correlation between weather changes and cyclists?':
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.bar(main_df['weathersit'], main_df['Total'], color='#00E8FF')
    ax.set_xlabel('Weather', fontsize=18, color='white')
    ax.set_ylabel('Number', fontsize=18, color='white')
    ax.set_title('Correlation between Weather Changes and Cyclists', color='white', fontsize=20)
    st.pyplot(fig)
    
    st.write("""
        Conclusion: There is a significant correlation between weather changes and bicycle use. Bicycle users prefer sunny weather and avoid heavy rainfall.
    """)

# Answer for patterns during seasons
elif qa_option == 'What patterns do cyclists make throughout the changing seasons?':
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.bar(main_df['season'], main_df['Total'], color='#00E8FF')
    ax.set_xlabel('Season', fontsize=18, color='white')
    ax.set_ylabel('Number', fontsize=18, color='white')
    ax.set_title('Bicycle Usage Patterns Across Seasons', color='white', fontsize=20)
    st.pyplot(fig)
    
    st.write("""
        Conclusion: Bicycle usage is higher during summer and significantly lower during winter and the rainy season.
    """)

# Footer section
st.caption('Copyright © Zharfan Fasya H 2024')
