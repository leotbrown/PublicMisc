import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import datetime as dt

today = dt.datetime(2022,6,29)
delta = dt.timedelta(7)
minuseven = today - delta

df = pd.read_csv(r'C:\Users\res_audit_PT.csv', thousands=',',decimal='.', )
df['CO_date'] = pd.to_datetime(df['CO_date'], format='%d/%m/%Y')
df['Res_Create'] = pd.to_datetime(df['Res_Create'], format='%d/%m/%Y')
df = df[df['CO_Month'].isin(['Jul', 'Aug'])]
df = df[(df['Res_Create'] >= minuseven) & (df['Res_Create'] <= today)]


cdata = df.groupby(['CO_date'], as_index=False)['Res_No'].count()
cdata.sort_values(by=['CO_date'], inplace=True)

data = cdata['Res_No']
scaler = StandardScaler()
np_scaled = scaler.fit_transform(data.values.reshape(-1,1))
data = pd.DataFrame(np_scaled)
model =  IsolationForest(contamination=float(0.1), max_samples='auto', bootstrap=True)

model.fit(data)
cdata['Anomaly_flag'] = pd.Series(model.predict(data))


fig, ax = plt.subplots(figsize=(10,6))

a = cdata.loc[cdata['Anomaly_flag'] == -1, ['CO_date', 'Res_No']] 

ax.plot(cdata['CO_date'], cdata['Res_No'], color='blue', label = 'Normal')
ax.scatter(a['CO_date'],a['Res_No'], color='red', label = 'Anomaly')
plt.legend()
plt.show()
plt.close()

cdata.to_csv(r'C:\Users\e771y6\Desktop\Misc\isotest.csv')

cdata.drop(['Res_No'], inplace=True, axis=1)

table = pd.merge(df, cdata, how='inner', on=['CO_date'])
table = table.loc[table['Anomaly_flag'] == -1]

table.to_csv(r'C:\Users\Misc\isotest2.csv')