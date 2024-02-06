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


@st.cache_data
def read_dataframe():
    Indian_df=pd.read_csv("../../Zomato/Indian_zomato.csv", encoding='ISO-8859-1')
    print(Indian_df)
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
  
    

st.title('Build for Bharat: Data as a service 🇮🇳')
st.write("Hello, 👋 Welcome to the dashboard by Dlayer team")
with st.sidebar:
    st.caption("<p style ='text-align:center'> Made with ❤️ by Eshika</p>",unsafe_allow_html=True )

Industry_list=['Food and Beverages', 'Fashion','Agriculture','Beauty and Personal Care']
Industry = st.selectbox('Select your Industry from the dropdown',Industry_list)

if Industry:
    if Industry!='Food and Beverages':
        st.write("We will be there soon...")
    else:
        st.write("Showing results for ",Industry)
        Indian_df=read_dataframe()
        # df_sample = Indian_df.sample(n = 100) 
        # df_sample.to_csv("Delivery.csv")
        # st.write(Indian_df.head(7))
        st.header("Analysis # 1")
        #TOP 5 CITIES in the business
        city_counts = Indian_df['City'].value_counts().reset_index()
        fig = px.bar(city_counts.head(5), x="count", y="City", orientation='h',color='City', title='Top 5 Cities with Maximum number of Restraunts') #df.sort_values('count')
        st.plotly_chart(fig)

        st.header("Analysis # 2")
        #TOP 5 CUISINES in the business
        Indian_df_cuisines_list=Indian_df['Cuisines'].tolist()
        Indian_df_cuisines_list=flattened_list(Indian_df_cuisines_list)
        Indian_df_Cuisines_df=pd.DataFrame(Indian_df_cuisines_list, columns=['Cuisine'])
        Indian_df_Cuisines_df=Indian_df_Cuisines_df['Cuisine'].value_counts().reset_index()
        fig = px.bar(Indian_df_Cuisines_df.head(5), x="count", y="Cuisine", orientation='h', color='Cuisine', title='Top 5 Famous Cuisines rated by Customers')
        st.plotly_chart(fig)

        st.header("Analysis # 3")
        # Apply the function to each group (city)
        df_filtered = Indian_df.groupby('City')['Average Cost for two'].apply(remove_outliers).reset_index(name='Average Cost for two')
        df_filtered.drop(['level_1'],axis=1,inplace=True)
        # st.write(df_filtered)
        print(df_filtered.columns)
        fig_scatter = px.scatter(df_filtered, x='City', y='Average Cost for two', color='City', title='Average Cost for Two in Different Cities', labels={'price': 'Price'})
        st.plotly_chart(fig_scatter)

        st.header("Analysis # 4")
        # average cost for 2 in the top 5 cities
        popular_cities=city_counts.head(5).sort_values(by='City',ascending=False)
        top_5_cities=popular_cities['City'].tolist()
        # top_5_cities_Indian_df=Indian_df[Indian_df['City'] in top_5_cities]
        top_5_cities_Indian_df = Indian_df[Indian_df['City'].isin(top_5_cities)]
        # st.write(top_5_cities_Indian_df)
        fig_scatter = px.scatter(top_5_cities_Indian_df, x='City', y='Average Cost for two', color='City', title='Average Cost for Two in Top 5 Cities with Maximum Restaurants', labels={'price': 'Price'})
        st.plotly_chart(fig_scatter)

        st.markdown("**For city level insights, click on the City Level insights from the left pane**")

        # st.markdown("**Want to know something specific about the analysis?Chat with our dashboard bot**")
        # st.text_area("Enter your question to ask Dashboard bot")

        with st.expander("Want to know something specific about the analysis?Chat with our dashboard bot"):
            st.text_area("Enter your question to ask Dashboard bot")
            st.markdown("**Integration with Generative AI bot in progress. Stay tuned...**")
            



st.divider()
st.caption("<p style ='text-align:center'> Made with ❤️ by Eshika</p>",unsafe_allow_html=True )






