import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import yfinance as yf
import plotly.graph_objects as go

st.title('FinLit 🔥')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# @st.cache
# def load_data(nrows):
#     data = pd.read_csv(DATA_URL, nrows=nrows)
#     lowercase = lambda x: str(x).lower()
#     data.rename(lowercase, axis='columns', inplace=True)
#     data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
#     return data

stock_tickers = pd.read_csv('s&p500.csv')
MMM = yf.Ticker(stock_tickers['Symbol'][0])
df = MMM.history(period = 'max')
df.reset_index(inplace=True)



data_load_state = st.text('Loading data...')
#data = load_data(10000)
data_load_state.text("Done!")

# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(data)

fig = go.Figure([go.Scatter(x=df['Date'], y=df['High'])])
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month",
                 stepmode="backward"),
            dict(count=6, label="6m", step="month",
                 stepmode="backward"),
            dict(count=1, label="YTD", step="year",
                 stepmode="todate"),
            dict(count=1, label="1y", step="year",
                 stepmode="backward"),
            dict(step="all")
        ])
    )
)
# st.subheader('Number of pickups by hour')
# hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(fig)

# Some number in the range 0-23
# hour_to_filter = st.slider('hour', 0, 23, 17)
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
#
# st.subheader('Map of all pickups at %s:00' % hour_to_filter)
# st.map(filtered_data)
