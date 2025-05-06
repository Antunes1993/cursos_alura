#%% Class 01
import json
import calendar
import numpy as np
import pandas as pd 
import plotly.express as px
from prophet import Prophet
import matplotlib.pyplot as plt
from prophet.plot import plot_plotly
from prophet.serialize import model_to_json
from prophet.plot import plot_components_plotly
from prophet.diagnostics import cross_validation
from prophet.diagnostics import performance_metrics
from prophet.plot import plot_cross_validation_metric
from sklearn.metrics import mean_squared_error, root_mean_squared_error  

#%% Loading Dataset
data_poluentes = pd.read_csv("..\\Data\\DS04 - Regressao - prevendo series temporais com prophet\\poluentes.csv", delimiter=',')
data_poluentes.head()

#%% Checking for missing values
print("Columns with data NaN")
data_poluentes.isna().sum()

#%% Converting date column to datetime format and plotting time series
data_poluentes.Data = pd.to_datetime(data_poluentes.Data)
fig = px.line(data_poluentes, x='Data', y='O3')
fig.show()

#%% Aggregating data by month for 2022
data_poluentes_2022 = data_poluentes[data_poluentes['Data'].dt.year == 2022]
data_poluentes_2022_monthly = data_poluentes_2022.groupby(data_poluentes_2022.Data.dt.month)['O3'].mean().reset_index()
data_poluentes_2022_monthly['Mês'] = data_poluentes_2022_monthly['Data'].apply(lambda x: calendar.month_abbr[x])
data_poluentes_2022_monthly

#%% Plotting monthly average of O3 levels for 2022
fig = px.bar(data_poluentes_2022_monthly, x='Mês', y='O3', title="Média de O3 ug/m3 por mês em 2022")
fig.update_layout(template='plotly_dark')
fig.show()

#%% Preparing data for Prophet model
data_prophet = pd.DataFrame()
data_prophet['ds'] = data_poluentes['Data']
data_prophet['y'] = data_poluentes['O3']
data_prophet.shape

#%% Training Prophet model
random_seed = 10
model = Prophet()
model.fit(data_prophet)
future = model.make_future_dataframe(periods=365, freq='D')
predictions = model.predict(future)

#%% Plotting predictions
fig = plot_plotly(model, predictions)
fig.show()

#%% Plotting components of the forecast
plot_components_plotly(model, predictions)


#%% Class 02
# Splitting data into training and test sets
len_training_data = int(len(data_prophet) * 0.8)
len_test_data = int(len(data_prophet) * 0.2)
print('Training data: ', len_training_data)
print('Test data: ', len_test_data)

# Creating training and test datasets
data_training = pd.DataFrame()
data_training['ds'] = data_prophet['ds'][:len_training_data]
data_training['y'] = data_prophet['y'][:len_training_data]

data_test = pd.DataFrame()
data_test['ds'] = data_prophet['ds'][len_training_data:]
data_test['y'] = data_prophet['y'][len_training_data:]

# Training Prophet model with training data
np.random.seed(4587)
model = Prophet()
model.fit(data_training)
future = model.make_future_dataframe(periods=len_test_data, freq='D')
predictions = model.predict(future)

#%% Plotting forecast with test data overlayed
fig = model.plot(predictions)
plt.plot(data_test['ds'], data_test['y'],'.r')
plt.show()

#%% Merging predictions with actual test data
data_predictions = predictions[['ds', 'yhat']] #yhat = model prediction
data_comparations = pd.merge(data_predictions, data_test, on='ds', how='inner')
data_comparations

#%% Calculating error metrics
mse = mean_squared_error(data_comparations['y'], data_comparations['yhat']).round(2)
rmse = root_mean_squared_error(data_comparations['y'], data_comparations['yhat']).round(2)
print(f'MSE:{mse}')
print(f'RMSE:{rmse}')


#%% Class 03
# Detecting and Removing Outliers
model = Prophet()
model.fit(data_prophet)
future = model.make_future_dataframe(periods=0, freq='D')
predictions = model.predict(future)
without_outliers = data_prophet[(data_prophet['y']> predictions['yhat_lower']) & (data_prophet['y'] < predictions['yhat_upper'])]
without_outliers.reset_index(drop=True, inplace=True)

#%% Splitting data without outliers into training and test sets
len_training_data = int(len(without_outliers) * 0.8)
len_test_data = int(len(without_outliers) * 0.2)
print('Training data: ', len_training_data)
print('Test data: ', len_test_data)

#%% Creating training and test datasets without outliers
data_training_without_outliers = pd.DataFrame()
data_training_without_outliers['ds'] = without_outliers['ds'][:len_training_data]
data_training_without_outliers['y'] = without_outliers['y'][:len_training_data]

data_test_without_outliers = pd.DataFrame()
data_test_without_outliers['ds'] = without_outliers['ds'][len_training_data:]
data_test_without_outliers['y'] = without_outliers['y'][len_training_data:]

# Training Prophet model with cleaned data
model = Prophet()
model.fit(data_training_without_outliers)
future = model.make_future_dataframe(periods=365, freq='D')
predictions = model.predict(future)
# Plotting forecast with test data overlayed
fig = model.plot(predictions)
plt.plot(data_test_without_outliers['ds'], data_test_without_outliers['y'],'.r')
plt.show()

#%% Merging predictions with actual test data
data_predictions = predictions[['ds', 'yhat']] #yhat = model prediction
data_comparations = pd.merge(data_predictions, data_test_without_outliers, on='ds', how='inner')
data_comparations

#%% Calculating error metrics
mse = mean_squared_error(data_comparations['y'], data_comparations['yhat']).round(2)
rmse = root_mean_squared_error(data_comparations['y'], data_comparations['yhat']).round(2)
print(f'MSE:{mse}')
print(f'RMSE:{rmse}')

#%% Increasing trend flexibility in Prophet model
model = Prophet(changepoint_prior_scale=0.5)
model.fit(data_training_without_outliers)
future = model.make_future_dataframe(periods=0, freq='D')
predictions = model.predict(future)
fig=model.plot(predictions)

#%% Calculating error metrics
fig=plot_components_plotly(model, predictions)
fig.show()

#%% Increasing seasonal flexibility in Prophet model
model = Prophet(changepoint_prior_scale=0.5, yearly_seasonality=20)
model.fit(data_training_without_outliers)
future = model.make_future_dataframe(periods=365, freq='D')
predictions = model.predict(future)
fig=model.plot(predictions)

#%% Plotting trend components
fig=plot_components_plotly(model, predictions)
fig.show()

#%% Plotting forecast with test data overlayed
fig = model.plot(predictions)
plt.plot(data_test_without_outliers['ds'], data_test_without_outliers['y'],'.r')
plt.show()


#%% Merging predictions with actual test data
data_predictions = predictions[['ds', 'yhat']] #yhat = model prediction
data_comparations = pd.merge(data_predictions, data_test_without_outliers, on='ds', how='inner')
data_comparations

#%% Calculating error metrics
mse = mean_squared_error(data_comparations['y'], data_comparations['yhat']).round(2)
rmse = root_mean_squared_error(data_comparations['y'], data_comparations['yhat']).round(2)
print(f'MSE:{mse}')
print(f'RMSE:{rmse}')

#%% Class 04 
data_cv = cross_validation(model, initial='365.25 days', period='45 days', horizon='90 days')
#%%
data_cv['cutoff'].unique()

#%% Checking metrics for the cross-validation 
data_p = performance_metrics(data_cv)
data_p.rmse.mean().round(2)

#%%
plot_cross_validation_metric(data_cv, metric='rmse');

#%%
with open('modelo_O3_prophet.json', 'w') as file_out:
    json.dump(model_to_json(model), file_out)
