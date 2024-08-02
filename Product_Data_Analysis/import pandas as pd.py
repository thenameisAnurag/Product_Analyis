import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load data from Google Sheets
sheet_name = "Dummy_Data"
sheet_id = "1mIYAIM8DTibovMeV8bvVDO-B9vgwApZTjyxIXXGFGQw"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
data = pd.read_csv(url)

# Drop empty rows and columns
data.dropna(how='all', axis=1, inplace=True)
data.dropna(how='all', axis=0, inplace=True)
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

# Drop rows with any missing values
data.dropna(how='any', axis=0, inplace=True)

# Convert timestamp to datetime
data['timestamp'] = pd.to_datetime(data['timestamp'])
Time_stamp = data['timestamp']
Hours = Time_stamp.dt.hour

# Plot distribution of hours
plt.figure(figsize=(10, 6))
plt.hist(Hours, bins=24, histtype='bar', edgecolor='black')
plt.xlabel('Hour of the Day')
plt.ylabel('Frequency')
plt.title('Distribution of Hours')
plt.xticks(range(24))
plt.show()

# Calculate time difference
Diff = data['option_time_spend'] - data['time_spend_on_att']
data['time_diff'] = Diff

# Extract day of the week
data['day_of_week'] = Time_stamp.dt.day_name()  

# Aggregate user engagement by day of the week
engagement_by_day = data.groupby('day_of_week').agg({
    'time_spend_on_att': 'mean',  
    'option_time_spend': 'mean',
    'option_id': 'count'
}).reset_index()

# Sort days of the week
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
engagement_by_day['day_of_week'] = pd.Categorical(engagement_by_day['day_of_week'], categories=day_order, ordered=True)
engagement_by_day = engagement_by_day.sort_values('day_of_week')

# Plot user engagement by day of the week
plt.figure(figsize=(12, 6))
sns.lineplot(data=engagement_by_day, x='day_of_week', y='time_spend_on_att', marker='o', label='Avg Time Spent on Attributes')
sns.lineplot(data=engagement_by_day, x='day_of_week', y='option_time_spend', marker='o', label='Avg Option Time Spent')
plt.xlabel('Day of the Week')
plt.ylabel('Average Value')
plt.title('User Engagement by Day of the Week')
plt.legend()
plt.grid(True)
plt.show()


threshold = 10 
data['conversion'] = np.where(data['option_time_spend'] > threshold, 1, 0)


attribute_stats = data.groupby('attribute_name').agg({
    'conversion': 'sum', 
    'attribute_id': 'count' 
}).reset_index()
attribute_stats['conversion_rate'] = (attribute_stats['conversion'] / attribute_stats['attribute_id']) * 100

option_stats = data.groupby('option_name').agg({
    'conversion': 'sum', 
    'option_id': 'count'  
}).reset_index()
option_stats['conversion_rate'] = (option_stats['conversion'] / option_stats['option_id']) * 100

plt.figure(figsize=(12, 6))
sns.barplot(data=attribute_stats, x='attribute_name', y='conversion_rate', palette='viridis')
plt.xlabel('Attribute Name')
plt.ylabel('Conversion Rate (%)')
plt.title('Conversion Rate by Attribute')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

