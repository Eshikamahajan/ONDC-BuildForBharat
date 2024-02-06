import streamlit as st

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
'''

fig = px.box(city_df, x='City', y='Average Cost for two', title='Price Range in Different Cities', labels={'price': 'Price'})
st.plotly_chart(fig) #Indian_df
fig = px.box(Indian_df, x='City', y='Average Cost for two', title='Price Range in Different Cities', labels={'price': 'Price'})
st.plotly_chart(fig) #Indian_df


fig = px.violin(Indian_df, x='City', y='Average Cost for two', title='Price Range for Different Cuisines', labels={'price': 'Price'})
st.plotly_chart(fig)

fig = px.line(city_df, x='City', y='Average Cost for two', title='Price Range in Different Cities', labels={'price': 'Price'})
st.plotly_chart(fig)
fig = px.line(Indian_df, x='City', y='Average Cost for two', title='Price Range for Different Cuisines', labels={'price': 'Price'})
st.plotly_chart(fig)'''