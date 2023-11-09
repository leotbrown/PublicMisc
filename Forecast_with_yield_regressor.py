import pandas as pd
import os.path
import teradata as td
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly

class Main:
    
    def __init__(self, country, start_date, end_date, periods):
        self.country = country
        self.start_date = start_date
        self.end_date = end_date
        self.periods = periods
        
    def retrieve_data(self, conn):
        SQLStr = (
            "SELECT "
            )
        
        data = pd.read_sql_query(SQLStr, conn)
        data['ds'] = pd.to_datetime(data['ds'], format='%Y-%m-%d')
        training_data = data.loc[data['ds'] <= self.end_date]
        
        self.training_data = training_data
        self.prediction_data = data
        
    def ph_forecast(self, destination_folder):
        model = Prophet()
        model.add_regressor('Yield', standardize=False)
        model.fit(self.training_data)
        
        future = self.prediction_data
        future.to_csv(r'C:\Users\test.csv')
        forecast = model.predict(future)
        
        fig1 = model.plot(forecast)
        fig2 = model.plot_components(forecast)
        
        figpath = os.path.join(destination_folder, f'{self.country}_fig1.png')
        fig1.savefig(figpath)
        figpath = os.path.join(destination_folder, f'{self.country}_fig2.png')
        fig2.savefig(figpath)

        plot_plotly(model, forecast)
        plot_components_plotly(model, forecast)
        filepath = os.path.join(destination_folder, f'{self.country}_Forecast.csv')
        
        forecast.to_csv(filepath)
        
udaExec = td.UdaExec (appName="Teradata", version="1.0", logConsole=False)
session = udaExec.connect(method='odbc',DSN='', username='',
                             password='');

model = Main('HR', '2020-01-01', '2023-03-30', 180)

model.retrieve_data(session)
model.ph_forecast(r'C:\Users')

session.close()

del model

print('Job done!')