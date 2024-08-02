import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


sheet_name = "Dummy_Data"
sheet_id = "1mIYAIM8DTibovMeV8bvVDO-B9vgwApZTjyxIXXGFGQw"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
data = pd.read_csv(url)

# Drop empty rows and columns
data.dropna(how='all', axis=1, inplace=True)
data.dropna(how='all', axis=0, inplace=True)
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

data.dropna(how='any', axis=0, inplace=True)

data['timestamp'] = pd.to_datetime(data['timestamp'])
data['day_of_week'] = data['timestamp'].dt.day_name()  


engagement_by_day = data.groupby('day_of_week').agg({
    'time_spend_on_att': 'mean',  
    'option_time_spend': 'mean',
    'option_id': 'count'        
}).reset_index()

day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
engagement_by_day['day_of_week'] = pd.Categorical(engagement_by_day['day_of_week'], categories=day_order, ordered=True)
engagement_by_day = engagement_by_day.sort_values('day_of_week')


plt.figure(figsize=(12, 6))
sns.lineplot(data=engagement_by_day, x='day_of_week', y='time_spend_on_att', marker='o', label='Avg Time Spent on Attributes')
sns.lineplot(data=engagement_by_day, x='day_of_week', y='option_time_spend', marker='o', label='Avg Option Time Spent')
plt.xlabel('Day of the Week')
plt.ylabel('Average Value')
plt.title('User Engagement by Day of the Week')
plt.legend()
plt.grid(True)
plt.show()

