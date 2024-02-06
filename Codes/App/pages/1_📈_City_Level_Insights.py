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
    page_title="City Level Insights",
    page_icon="👩🏻‍💻"
)

@st.cache_data
def read_dataframe():
    Indian_df=pd.read_csv("../../Zomato/Indian_zomato.csv", encoding='ISO-8859-1')
    # st.write(Indian_df)
    ## RENAMING AND DROPPING THE COLUMNS
    Indian_df.rename(columns={'Unnamed: 0': 'ID'}, inplace=True)
    Indian_df.drop(['Restaurant ID','Country Code','Locality','Currency','Rating color','Switch to order menu'],axis=1,inplace=True)#df.drop(['C', 'D'], axis=1)
    return Indian_df

@st.cache_data
def city_wise_df(city):
    name_df='df_'+str(city)
    name_df=Indian_df[Indian_df['City']==city]
    return name_df

@st.cache_data  
def flattened_list(sample_list):
    flattened_items_list = [items.strip() for items in sample_list for items in items.split(',')] # getting a flattened list of cuisines
    flattened_items_list=flattened_items_list
    #print(len(flattened_cuisine_list))
    return flattened_items_list

def remove_outliers(group):
    q_low = group.quantile(0.01)
    q_hi = group.quantile(0.99)
    return group[(group > q_low) & (group < q_hi)]

def remove_outliers_df(df):
    q_low = df['Average Cost for two'].quantile(0.01)
    q_hi = df['Average Cost for two'].quantile(0.99)
    return df[(df['Average Cost for two'] > q_low) & (df['Average Cost for two'] < q_hi)]


def full_graph(city_df_Cuisines_df,city_df_without_outliers):
    st.header("Analysis # 5")
    fig = px.bar(city_df_Cuisines_df.head(25), x="count", y="Cuisine", orientation='h', color='Cuisine', title='Different Cuisines served in the Selected City')
    st.plotly_chart(fig)

    st.header("Analysis # 6")
    fig = px.bar(city_df_without_outliers, x='Cuisines', y='Average Cost for two', title='Average Cost for Two in the Selected City',labels={'price': 'Price'})
    st.plotly_chart(fig)


Indian_df=read_dataframe()
City_list=Indian_df['City'].tolist()
City_list=flattened_list(City_list)
Unique_City_list=set(City_list)
st.write("<h3> Let's Explore the data at City level</h3>",unsafe_allow_html=True )
st.write(" ")
city_option = st.selectbox( 'Select a city that you wish to analyse', Unique_City_list)
st.write('You selected:', city_option)
st.write(" ")

if city_option:
    city_df=city_wise_df(city_option)
    # st.write(city_df)
    #TOP 5 CUISINES in the business
    city_df_cuisines_list=city_df['Cuisines'].tolist()
    city_df_cuisines_list=flattened_list(city_df_cuisines_list)
    city_df_Cuisines_df=pd.DataFrame(city_df_cuisines_list, columns=['Cuisine'])
    city_df_Cuisines_df=city_df_Cuisines_df['Cuisine'].value_counts().reset_index()
    city_df_without_outliers = remove_outliers_df(city_df)

    if len(set(city_df_cuisines_list))>15:
        st.warning("Since there are more than 15 Cuisines served in this city, Displaying results for top 10 served Cuisines")
        st.header("Analysis # 5")
        fig = px.bar(city_df_Cuisines_df.head(10), x="count", y="Cuisine", orientation='h', color='Cuisine', title='Famous Cuisines served in the Selected City')
        st.plotly_chart(fig)

        top_5_Cuisines=city_df_Cuisines_df.head(5)['Cuisine'].tolist()
        mask = city_df_without_outliers['Cuisines'].apply(lambda x: any(cuisine in x for cuisine in top_5_Cuisines))
        filtered_df = city_df_without_outliers[mask]
        st.header("Analysis # 6")
        fig = px.bar(filtered_df, x='Cuisines', y='Average Cost for two', title='Average Cost for Two in the Selected City',labels={'price': 'Price'})
        st.plotly_chart(fig)

        full_visual=st.button("See visualizations for complete data in the city")
        if full_visual:
            full_graph(city_df_Cuisines_df,city_df_without_outliers)
        else:
            pass

    else:
       full_graph(city_df_Cuisines_df,city_df_without_outliers)


st.divider()
st.caption("<p style ='text-align:center'> Made with ❤️ by Eshika</p>",unsafe_allow_html=True )

with st.sidebar:
    st.caption("<p style ='text-align:center'> Made with ❤️ by Eshika</p>",unsafe_allow_html=True )


    

    # # average cost for 2 in the top 5 cities
    # popular_cities=city_counts.head(5).sort_values(by='City',ascending=False)
    # top_5_cities=popular_cities['City'].tolist()
    # # top_5_cities_Indian_df=Indian_df[Indian_df['City'] in top_5_cities]
    # top_5_cities_Indian_df = Indian_df[Indian_df['City'].isin(top_5_cities)]
    # # st.write(top_5_cities_Indian_df)
    # fig_scatter = px.scatter(top_5_cities_Indian_df, x='City', y='Average Cost for two', color='City', title='Average cost for 2 in Different Cities', labels={'price': 'Price'})
    # st.plotly_chart(fig_scatter)




    






