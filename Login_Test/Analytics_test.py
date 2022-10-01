import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime
from dateutil.relativedelta import relativedelta

def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

def app():
	# s&p500.csv
	ticker_list = pd.read_csv('s&p500.csv')
	selected_stock = st.sidebar.selectbox('Stock', ticker_list)
	
	stock_data = yf.Ticker(selected_stock)
	stock_name = stock_data.info['shortName']
	st.title(f"Showing Analytics for {stock_name}")
	
	PE = round(stock_data.info['trailingPE'],2)
	market_cap = round(stock_data.info['marketCap'],2)
	market_cap = human_format(market_cap)
	week_52_low = round(stock_data.info['fiftyTwoWeekLow'],2)
	week_52_low = "{:,}".format(week_52_low)
	week_52_high = round(stock_data.info['fiftyTwoWeekHigh'],2)
	week_52_high = "{:,}".format(week_52_high)
	

	df = stock_data.history(period='max')
	df.reset_index(inplace=True)
	
# 	sentence = stock_data.info['longBusinessSummary']
	sentence = '3M (originally the Minnesota Mining and Manufacturing Company) is an American multinational conglomerate operating in the fields of industry, worker safety, U.S. health care, and consumer goods.'
	st.subheader("About the Company")
	
	st.write(sentence)
	
	st.subheader("Financial Ratios")
	
	col1, col2, col3, col4 = st.columns(4)
	label_1 = "Market Cap"
	col1.metric(label_1, market_cap, delta=None, delta_color="normal", help=None)
	label_2 = "PE Ratio"
	col2.metric(label_2, PE, delta=None, delta_color="normal", help=None)
	label_3 = "52 Week High"
	col3.metric(label_3, week_52_high, delta=None, delta_color="normal", help=None)
	label_4 = "52 Week Low"
	col4.metric(label_4, week_52_low, delta=None, delta_color="normal", help=None)
	
	
	
# 	fig = go.Figure([go.Scatter(x=df['Date'], y=df['Close'])])

	fig = go.Figure(data=[go.Candlestick(x=df['Date'],
		    open=df['Open'],
		    high=df['High'],
		    low=df['Low'],
		    close=df['Close'])])
	fig.update_layout(
	    title=f"Price Chart for {stock_data.info['symbol']}",
	    xaxis_title="Date",
	    yaxis_title="Price (USD)"
	)
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
	fig.update_layout(xaxis=dict(rangeselector = dict(font = dict( color = "black"))))
	st.plotly_chart(fig, use_container_width=True)
	
	one_yrs_ago = datetime.now() - relativedelta(years=1)
	date = one_yrs_ago.date()
	
	for i in df['Date']:
		if i == date:
			ans = df.loc[df['Date'] == i].index[0]
			break
	one_year_date = df['Date'].iloc[ans:]
	one_year_vol = df['Volume'].iloc[ans:]
	vol_chart = go.Figure([go.Scatter(x=one_year_date, y=one_year_vol,line=dict(color="#FF0000"))])
	vol_chart.update_xaxes(
	    rangeslider_visible=True
	)
	vol_chart.update_layout(title_text="Daily Volume Chart")

	st.plotly_chart(vol_chart, use_container_width=True)

