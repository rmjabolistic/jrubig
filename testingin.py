python3.7 -m venv ~/.streamlit_ve
source ~/.streamlit_ve/bin/activate
pip install -U pip
pip install streamlit
pip install networkx
pip install mysql-connector-python

pip install pymysql

pip install mysqlclient

import streamlit as st 
import mysql.connector
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from fbprophet.plot import plot_components_plotly
from  fbprophet.diagnostics import cross_validation
from  fbprophet.diagnostics import performance_metrics
from plotly import graph_objs as go
import pandas as pd
import numpy as np


st.title("Predictive Analytics")

product = ("ALL","Big Buko Pie / Box","Mini Buko Pie Box","Mini Buko Pie Piece","Macaroons","Macapuno Balls","Coffee",
           "Buko Juice 1L Bottle","Buko Shake 1L Bottle","Macapuno Shake 1L Bottle","Buko Juice 12oz Cup","Buko Juice 16oz Cup",
           "Buko Juice 22oz Cup","Buko Shake 12oz Cup","Buko Shake 16oz Cup","Buko Shake 22oz Cup","Hot Choco","Macapuno Shake 12oz Cup",
           "Macapuno Shake 16oz Cup","Macapuno Shake 22oz Cup","Buko Juice 350ml Bottle","Buko Shake 350ml Bottle",
           "Buko Shake 500ml Bottle","Macapuno Shake 350ml Bottle","Macapuno Shake 500ml Bottle")




selected_product = st.selectbox("Select product for prediction",product)

n_days = st.slider('Days of prediction:', 1, 31)

connection = mysql.connector.connect(host = 'sql6.freesqldatabase.com',user = 'sql6450411', passwd = 'HdqLbnNupu', db = 'sql6450411')


#sales = cur.execute(""" SELECT * FROM sales_order WHERE date >= "2021-03-01 00:00:00" and name = %s """, (product, ))

if selected_product == "ALL":
  sales = pd.read_sql_query("SELECT * FROM sales_order WHERE date >= '2021-03-01 00:00:00'",  connection)
else:
  sales = pd.read_sql_query("SELECT * FROM sales_order WHERE date >= '2021-03-01 00:00:00' and name = '%s' " % selected_product, connection)



sales_new = sales[['qty','date']]
sales_new['date'] = pd.to_datetime(sales_new['date']).dt.date
sales_new = sales_new.rename(columns = {'qty': 'y', 'date': 'ds'}, inplace = False)
sales_new = sales_new.groupby('ds')['y'].sum()
sales_new = pd.DataFrame(sales_new)
sales_new.reset_index(level=0, inplace=True)


m = Prophet(interval_width=0.88).add_seasonality(name='monthly', period= 30.5,fourier_order=14)
model = m.fit(sales_new)

future = m.make_future_dataframe(periods= n_days,freq='D')
forecast = m.predict(future)

plot1 = plot_plotly(m, forecast)
plot1

plot2  = plot_components_plotly(m, forecast)
plot2

