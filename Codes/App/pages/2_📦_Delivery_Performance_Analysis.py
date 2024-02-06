import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from wordcloud import WordCloud
warnings.filterwarnings("ignore")

pd.options.display.max_columns = None
pd.options.display.max_rows = None

st.set_page_config(
    page_title="Logistics Analysis",
    page_icon="👩🏻‍💻"
)

@st.cache_data
def read_dataframe():
    logistics_df=pd.read_csv("../../Logistics/DeliveryPointsGenAI.csv")
    # st.write(logistics_df)
    # ## RENAMING AND DROPPING THE COLUMNS
    # Indian_df.rename(columns={'Unnamed: 0': 'ID'}, inplace=True)
    # Indian_df.drop(['Restaurant ID','Country Code','Locality','Currency','Rating color','Switch to order menu'],axis=1,inplace=True)#df.drop(['C', 'D'], axis=1)
    return logistics_df

@st.cache_data
def wordcloud(sample_list):
    wordcloud = WordCloud(width=700, height=400, background_color='white', normalize_plurals=False).generate(' '.join(sample_list))
    fig, ax = plt.subplots(figsize = (12, 8))
    ax.imshow(wordcloud)
    plt.gca().add_patch(plt.Rectangle((0, 0), 800, 400, linewidth=2, edgecolor='g', facecolor='none'))
    plt.axis("off")
    st.pyplot(fig)

@st.cache_data  
def flattened_list(sample_list):
    flattened_cuisine_list = [Cuisines.strip() for Cuisines in sample_list for Cuisines in Cuisines.split(',')] # getting a flattened list of cuisines
    flattened_cuisine_list=flattened_cuisine_list
    #print(len(flattened_cuisine_list))
    return flattened_cuisine_list

logistics_df=read_dataframe()

st.write("<h3> Let's Explore the Logistics Data in Delhi</h3>",unsafe_allow_html=True )
st.write(" ")

Agencies=logistics_df['AgencyName'].tolist()
agencies_list=flattened_list(Agencies)
Unique_agencies_list=set(agencies_list)

wordcloud(Unique_agencies_list)


# Combine "Destination" and "City" into a new column "FullDestination"
logistics_df['FullDestination'] = logistics_df['Destination'] + ', ' + logistics_df['City']

# Basic Analysis Examples:

# 1. Average Delivery Time Analysis
# average_delivery_time = logistics_df['AverageDeliveryTime'].mean()
# st.write("\nAverage Delivery Time across all agencies:", average_delivery_time)

# # 2. Delivery Rating Analysis
# average_delivery_rating = logistics_df['DeliveryRating'].mean()
# st.write("Average Delivery Rating across all agencies:", average_delivery_rating)

# # 3. Delivery Charges Analysis
# average_delivery_charges = logistics_df['DeliveryCharges'].mean()
# st.write("Average Delivery Charges across all agencies:", average_delivery_charges)

# 4. Destination-wise Analysis
destination_analysis = logistics_df.groupby('Destination').agg({
    'AverageDeliveryTime': 'mean',
    'DeliveryRating': 'mean',
    'DeliveryCharges': 'mean'
}).reset_index()
st.write("\nDestination-wise Analysis:")
st.write(destination_analysis)

st.header("Analysis # 7")
# 1. Bar plot for Average Delivery Time, Rating, and Charges
fig = px.bar(logistics_df, x='AgencyName', y='AverageDeliveryTime', title='Average Delivery Time - Agency Wise',color='Destination')
st.plotly_chart(fig)

st.header("Analysis # 8")
fig = px.bar(logistics_df, x='AgencyName', y='DeliveryRating', title='Average Delivery Rating - Agency Wise',color='Destination')
st.plotly_chart(fig)

st.header("Analysis # 9")
fig = px.bar(logistics_df, x='AgencyName', y='DeliveryCharges', title='Average Delivery Charges - Agency Wise',color='Destination')
st.plotly_chart(fig)

st.header("Analysis # 10")
fig = px.bar(destination_analysis, x='Destination', y='AverageDeliveryTime', title='Average Delivery Time by Destination',color='Destination')
st.plotly_chart(fig)

st.header("Analysis # 11")
fig = px.bar(destination_analysis, x='Destination', y='DeliveryRating', title='Average Delivery Rating by Destination',color='Destination')
st.plotly_chart(fig)

st.header("Analysis # 12")
fig = px.bar(destination_analysis, x='Destination', y='DeliveryCharges', title='Average Delivery Charges by Destination',color='Destination')
st.plotly_chart(fig)


st.divider()
st.caption("<p style ='text-align:center'> Made with ❤️ by Eshika</p>",unsafe_allow_html=True )

with st.sidebar:
    st.caption("<p style ='text-align:center'> Made with ❤️ by Eshika</p>",unsafe_allow_html=True )
