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
    page_title="ONDC Hackathon Dashboard",
    page_icon="👩🏻‍💻"
)

with st.sidebar:
    st.write("Hello")

@st.cache_data
def read_dataframe():
    Indian_df=pd.read_csv("../../Zomato/Indian_zomato.csv", encoding='ISO-8859-1')
    print(Indian_df)
    return Indian_df

@st.cache_data
def city_wise_df(city):
    name_df='df_'+str(city)
    name_df=Indian_df[Indian_df['City']==city]
    return name_df

@st.cache_data
def wordcloud(sample_list):
    wordcloud = WordCloud(width=700, height=400, background_color='white').generate(' '.join(sample_list))
    fig, ax = plt.subplots(figsize = (10, 8))
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

@st.cache_data
def avg_cost(df,Cuisine_to_search):
    print("\n")
    minimum=maximum=average=0
    st.write(" ")
    text="<h5> Finding the pricing for "+ Cuisine_to_search+" </h5>"
    st.write(text,unsafe_allow_html=True )
    mask = df.Cuisines.apply(lambda x: Cuisine_to_search in x)
    df = df[mask]
    if df.empty:
        st.error("Cuisine not found" )
    else:
        price_range_stats = df.groupby('City')['Average Cost for two'].agg(['min', 'max'])
        minimum=price_range_stats['min'].iloc[0]
        maximum=price_range_stats['max'].iloc[0]
        price_mean_stats = df.groupby('City')['Average Cost for two'].mean()
        average=price_mean_stats.values[0]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Min price for the selected Cuisine :",minimum)
        with col2:
            st.write("Average price for the selected Cuisine : ",average)
        with col3:
            st.write("Max price for the selected Cuisine : ",maximum)
  
    
@st.cache_data   
def get_price_range(Cost):
    if Cost>=0 and Cost<=450:
        return 1 
    elif Cost>=451 and Cost<=950:
        return 2
    elif Cost>=951 and Cost<=1500:
        return 3
    elif Cost>=1501 and Cost<=2000:
        return 4
    else:
        return 5
    

Indian_df=read_dataframe()

#### Preprocessing 

## CALCULATING PRICE RANGE BASED ON AVERAGE COST OF TWO, 0 TO 5 WHERE 0 IS AFFORDABLE AND 5 IS EXPENSIVE
# price_range_stats = Indian_df.groupby('Price range')['Average Cost for two'].agg(['min', 'max'])
Indian_df['Price range'] = Indian_df['Average Cost for two'].apply(get_price_range)
## RENAMING AND DROPPING THE COLUMNS
Indian_df.rename(columns={'Unnamed: 0': 'ID'}, inplace=True)
Indian_df.drop(['ID','Country Code','Locality','Currency','Rating color','Switch to order menu'],axis=1,inplace=True)#df.drop(['C', 'D'], axis=1)

#Title
st.title('ONDC Data as a service PS 🤖')
#Welcoming message
st.write("Hello, 👋 We are analysing Restraunts Data under food chain supply.")

st.write("A glimpse of the data")
st.write(Indian_df.head(7))

# CITY WISE RESTRAUNT COUNT
city_counts = Indian_df['City'].value_counts().reset_index()
st.write("<h3> City wise restraunt count</h3>",unsafe_allow_html=True )
# st.write(city_counts)
city_counts_T = city_counts.T
st.write(city_counts_T)

import streamlit as st

City_list=Indian_df['City'].tolist()
City_list=flattened_list(City_list)
Unique_City_list=set(City_list)

Cuisines_list=Indian_df['Cuisines'].tolist()
Cuisines_list=flattened_list(Cuisines_list)
Unique_Cuisines_list=set(Cuisines_list)

col1, col2 = st.columns(2)

with col1:
   
   st.write("<h3> Top Cities with highest number of Restraunts</h3>",unsafe_allow_html=True )
   wordcloud(City_list)
   st.write(" ")

with col2:
    ##CUISINES
    st.write("<h3> Cuisines served in the Restraunts</h3>",unsafe_allow_html=True )
    wordcloud(Cuisines_list)
    st.write(" ")


st.write("<h3> Let's Explore the data at City level</h3>",unsafe_allow_html=True )
st.write(" ")
city_option = st.selectbox(
    'Select a city that you wish to analyse',
    Unique_City_list)

st.write('You selected:', city_option)
st.write(" ")

city_df=city_wise_df(city_option)
city_df_cuisines_list=city_df['Cuisines'].tolist()
city_df_cuisines_list=flattened_list(city_df_cuisines_list)
Unique_city_df_cuisines_list=set(city_df_cuisines_list)
text="<h3> Cuisines served in "+city_option+" </h3>"
st.write(text,unsafe_allow_html=True )
wordcloud(city_df_cuisines_list)
# st.write(city_df.columns)

colA,colB=st.columns(2)
with colA:

    fig_scatter = px.scatter(Indian_df.head(10), x='City', y='Average Cost for two', color='City', title='Price in Different Cities', labels={'price': 'Price'})
    st.plotly_chart(fig_scatter)

with colB:

    fig = px.violin(city_df.head(10), x='City', y='Average Cost for two', title='Price Range in the selected city', labels={'price': 'Price'})
    st.plotly_chart(fig)


st.write(" ")
text="<h3> Find the pricing for a particular Cuisine in "+ city_option+" </h3>"
st.write(text,unsafe_allow_html=True )

# Cuisine=st.text_input("Enter the Cuisine to search","Mughlai")
Cuisine = st.selectbox('Select the Cuisine you wish to search',Unique_city_df_cuisines_list)
if Cuisine:
    Cuisine_to_Search=Cuisine
    avg_cost(city_df,Cuisine_to_Search) 

st.divider()
st.caption("<p style ='text-align:center'> Made with ❤️ by Eshika</p>",unsafe_allow_html=True )
