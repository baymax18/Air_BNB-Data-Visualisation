import pandas as pd
import streamlit as st
import geopandas as gpd
import pydeck as pdk
import plotly.express as px




df = pd.read_csv('F:/AIR_BNB/airbnb_DATA.csv')



st.set_page_config(page_title="AirBNB",layout='wide')
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        color: violet;
    }
    </style>
    <h1 class="title">AirBNB Data Visualisation</h1>
    """,
    unsafe_allow_html=True
)


col1,col2=st.columns([1.2,4.55])

with col1:
   country = col1.multiselect("Select the Country:", options = df['Country'].unique(),default = df['Country'].unique())
   room = col1.multiselect("Select the Room_Type:", options = df['Room_type'].unique(),default = df['Room_type'].unique())
   Property = col1.multiselect("Select the Property_type:", options = df['Property_type'].unique(),default = df['Property_type'].unique())
   cancel = col1.multiselect("Select the Cancellation_policy:", options = df['Cancellation_policy'].unique(),default = df['Cancellation_policy'].unique())

with col2:
   if country or room or Property or cancel:
    df1 = (df['Country'].isin(country)) & (df['Room_type'].isin(room)) & (df['Property_type'].isin(Property)) & (df['Cancellation_policy'].isin(cancel))
    filtered_df = df[df1][['Name', 'Description', 'Property_type', 'Room_type', 'Bed_type',
                           'Min_nights', 'Max_nights', 'Cancellation_policy', 'Accomodates',
                           'Total_bedrooms', 'Total_beds', 'Availability_365', 'Price', 'neighbourhood', 
                           'No_of_reviews', 'Review_scores', 'Amenities', 'Host_name', 'Street', 'Country','Longitude', 'Latitude']]
    if not filtered_df.empty:
         filtered_df = filtered_df.reset_index(drop=True)
         filtered_df.columns = filtered_df.columns.str.title()
         # filtered_df['S.No'] = range(1, len(filtered_df) + 1)
         col2.dataframe(filtered_df)

         st.subheader(':violet[Geospatial Visualisation]' )
         fig = px.scatter_geo(filtered_df, lat='Latitude', lon='Longitude', size = 'Review_Scores',
                              hover_name='Name',
                              hover_data={'Latitude': False, 'Longitude': False, 'Review_Scores': False, 'Price': True, 'Country': True},
                              projection='natural earth',width = 900, height = 700)
         fig.update_geos(
                        showcountries=True,
                        countrycolor="Black",
                        showcoastlines=True,
                        coastlinecolor="Black",
                        showland=True,
                        landcolor="lightgray",
                        showocean=True,
                        oceancolor="lightblue"
                        )
         st.plotly_chart(fig)
    else:
       st.header(":red[Please try other combinations]")