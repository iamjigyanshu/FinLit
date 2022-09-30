import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime
from dateutil.relativedelta import relativedelta


def app():
	# s&p500.csv
	ticker_list = pd.read_csv('s&p500.csv')
	selected_stock = st.sidebar.selectbox('Stock', ticker_list)
	
	stock_data = yf.Ticker(selected_stock)
	stock_name = stock_data.info['shortName']
	st.title(f"Showing Analytics for {stock_name}")

	df = stock_data.history(period='max')
	df.reset_index(inplace=True)
	
	sentence = stock_data.info['longBusinessSummary']
	st.subheader("About the Company")
	st.write(sentence)
	
	fig = go.Figure([go.Scatter(x=df['Date'], y=df['Close'])])
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
	fig.update_layout(title_text="Closing Price Chart")
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
	vol_chart.update_layout(title_text="Daily Volume Chart")
	fig.update_layout(xaxis=dict(rangeselector = dict(font = dict( color = "black"))))
	st.plotly_chart(vol_chart, use_container_width=True)

