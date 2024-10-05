import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')
import os

st.write(os.getcwd())

# Membuatkan function untuk manipulasi dataframe

def byhour(df):
    hourly_rental = df.groupby(by='hour')['Total'].mean()
    return hourly_rental

def bymonth(df):
    monthly_rental = df.groupby(by='month')['Total'].mean()
    return monthly_rental

# import dataframe
day_df = pd.read_csv('submission/dashboard/day_modif_df.csv')
hour_df = pd.read_csv('submission/dashboard/hour_modif_df.csv')
season_df = pd.read_csv('submission/dashboard/melt_season_df.csv')
weather_df = pd.read_csv('submission/dashboard/melt_weathersit_df.csv')

day_df['date_day'] = pd.to_datetime(day_df['date_day'])
hour_df['date_day'] = pd.to_datetime(hour_df['date_day'])


# Filter data
min_date = hour_df["date_day"].min()
max_date = hour_df["date_day"].max()

with st.sidebar:
    # Menambahkan logo 
    st.image('https://raw.githubusercontent.com/fasya11/image/refs/heads/main/Desain%20tanpa%20judul.jpg', width=300)
    st.header('Bike Sharing')
    st.markdown("\n")
    
    
    st.markdown("""
    <div style="text-align: justify">
        Select a date 
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("\n")
    
    # Menjadikan start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Range Time',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
main_df = hour_df[(hour_df["date_day"] >= str(start_date)) & 
                (hour_df["date_day"] <= str(end_date))]

# Menyiapkan dataframe untuk buat grup
byhour_df = byhour(main_df)
bymonth_df = bymonth(hour_df)

st.header('Bike Sharing Analysis')
st.subheader('The Dashboard')
st.markdown("""
<div style="text-align: justify">
  This dashboard presents visual data related to bike usage based on time, month, season, and weather conditions. The information provides a comprehensive view of bike usage patterns, enabling users to understand trends, seasonal variations, and the impact of weather on bike activity.

</div>
""", unsafe_allow_html=True)

st.markdown("\n")

# Menampilkan Daily Rental

date_range = f"{start_date} – {end_date}"

# Menggunakan replace
date_range_slash = date_range.replace("-", "/")

st.subheader(f'Daily Bicycle Users {date_range_slash}')


col1, col2, col3 = st.columns(3)

with col1:
    casual_user = main_df.casual.sum()
    st.metric("Casual Rental", value=casual_user)

with col2:
    registered_user = main_df.registered.sum()
    st.metric("Register Rental", value=registered_user)
    
with col3:
    Total_user = main_df.Total.sum()
    st.metric("Total Rental", value=Total_user)

st.markdown("\n")
st.markdown("\n")

st.header('Data Analysis')
analysis_option = st.selectbox('Choose Analysis',
                      ['Bike Rental and Revenue per Month',
                       'Bike Rental Distribution Per Hour',
                       'Bike Rental Distribution Per Season',
                       'Bike Rental Distribution Per Weather',
                       ])

if analysis_option == 'Bike Rental and Revenue per Month':
    st.subheader('Average Monthly Bike Rental Users')

    # Membuat plot Rata-rata Pengguna Sepeda selama sebulan

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.bar(bymonth_df.index, bymonth_df.values, color='#00E8FF')
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)

    # Menjadikan background grafik menjadi hitam
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#262730')

    # Menjadikan warna label dan ticks 
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    # Membuat tambahan label x, label y, dan judul
    ax.set_xlabel('Month', color='white', fontsize=18)
    ax.set_ylabel('Average', color='white', fontsize=18)

    # Menampilkan plot  
    st.pyplot(fig)

    with st.expander("See explanation"):
        st.write(
            """Based on data from 2011 to 2012, bicycle usage trends show an increase from the beginning of the year 
            to the middle of the year, especially around June. From June to September, it can be seen that bicycle use 
            tends to remain stable, but begins to decline in October until the end of the year.
            """)


elif analysis_option == 'Bike Rental Distribution Per Hour':
    
    st.subheader(f'`Average Hourly Bicycle Riders')
    # Memplot rata-rata pengguna setiap jam
        
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.bar(byhour_df.index, byhour_df.values, color='#00E8FF')
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)

    # Membuat background grafik menjadi hitam
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#262730')

    # Membuat warna label dan ticks 
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    # Menambahkan label x, label y, dan judul
    ax.set_xlabel('Hour', color='white', fontsize=18)
    ax.set_ylabel('Average', color='white', fontsize=18)

    # Menampilkan plot 
    st.pyplot(fig)

    with st.expander("See explanation"):
        st.write(
            """On average, cyclists experience a notable increase at two specific times,
            i.e. during commuting hours around 8:00 am, and during commuting hours around 5:00 pm.
            """
        )

elif analysis_option == 'Bike Rental Distribution Per Season':

    st.subheader(f'Number of Bicycle Users by Season')
    #Membuat plot pengguna berdasarkan musim

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.bar(main_df['season'], main_df['Total'], color='#00E8FF')
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)

    # Membuat background grafik menjadi hitam
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#262730')

    # Mengubah warna label dan ticks jika diperlukan
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    # Menambahkan label x, label y, dan judul
    ax.set_xlabel('Season', color='white', fontsize=18)
    ax.set_ylabel('Number', color='white', fontsize=18)
    ax.set_title('Number of Bicycle Users by Season', color='white', fontsize=20)

    # Tampilkan plot menggunakan st.pyplot()
    st.pyplot(fig)

    with st.expander("See explanation"):
        st.write(
            """Based on data from 2011 to 2012, the highest number of bicycle users occurred in the *summer* season and the lowest number of bicycle users occurred in the *winter* season.
            and the lowest number of bicycle users occurred in the *winter* season. The graph also shows a *right-skewed distribution*.
            """
        )


elif analysis_option == 'Bike Rental Distribution Per Weather':

    st.subheader(f'Number of Bicycle Users by Weather')
    #Plotting pengguna berdasarkan cuaca

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.bar(main_df['weathersit'], main_df['Total'], color='#00E8FF')
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)

    # Mengubah background grafik menjadi hitam
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#262730')

    # warna label dan ticks diubah
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    # Membuat label x, label y, dan judul
    ax.set_xlabel('Weather', color='white', fontsize=18)
    ax.set_ylabel('Number', color='white', fontsize=18)
    ax.set_title('Number of Bicycle Users by Weather', color='white', fontsize=20)

    # Menampilkan plot 
    st.pyplot(fig)

    with st.expander("See explanation"):
        st.write(
            """Based on data from 2011 to 2012, the highest number of bicycle users occurred during *clear* weather.
            and the lowest number of bicycle users occurred during heavy precipitation*. The graph also shows a *left-skewed distribution*.
            """
        )

st.subheader(f'Question and Answer')
analysis_option = st.selectbox('The Question',
                      ['What is the correlation between weather changes and cyclists?',
                       'What patterns do cyclists make throughout the changing seasons?',
                      ])

if analysis_option == 'What is the correlation between weather changes and cyclists?':

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.bar(main_df['weathersit'], main_df['Total'], color='#00E8FF')
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)

    ax.set_xlabel('Weather', color='white', fontsize=18)
    ax.set_ylabel('Number', color='white', fontsize=18)
    ax.set_title('correlation between weather changes and cyclists', color='white', fontsize=20)

    st.pyplot(fig)
    st.markdown("\n")

    st.write("""
            Conclution question 1: The correlation between weather changes and bicycle use is 
             significant. Bicycle users prefer to ride when 
             the weather is sunny and decrease when the weather is heavy rainfall.
            """)
    
elif analysis_option == 'What patterns do cyclists make throughout the changing seasons?':
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.bar(main_df['season'], main_df['Total'], color='#00E8FF')
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)

    # Membuat background grafik menjadi hitam
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#262730')

    # Mengubah warna label dan ticks jika diperlukan
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    # Menambahkan label x, label y, dan judul
    ax.set_xlabel('Season', color='white', fontsize=18)
    ax.set_ylabel('Number', color='white', fontsize=18)
    ax.set_title('Number of Bicycle Users by Season', color='white', fontsize=20)

    # Tampilkan plot menggunakan st.pyplot()
    st.pyplot(fig)
    
    st.markdown("\n")
    st.write("""
            Conclution question 2: The resulting pattern is 
             that the number of bicycle users is higher 
            in the summer and lower in the rainy season.
            """)


st.caption('Copyright © Zharfan Fasya H 2024')

    
