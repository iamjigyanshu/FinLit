import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import plotly.graph_objects as go

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
	
	volume_chart = px.area(df['Volume'], 
                            title='Stock Daily Volume', 
                            color_discrete_map={'Volume':'red'} , 
                            width=800, height=400)
	st.plotly_chart(volume_chart, use_container_width=True)
# 	volume_chart.show()
