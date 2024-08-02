import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px


def read_and_clean_data(sheet_name, sheet_id):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    data = pd.read_csv(url)
    data.dropna(how='all', axis=1, inplace=True)
    data.dropna(how='all', axis=0, inplace=True)
    data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
    data.dropna(how='any', axis=0, inplace=True)
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    return data

def time_analysis(data):
    Time_stamp = data['timestamp']
    Hours = Time_stamp.dt.hour
    plt.figure(figsize=(10, 6))
    plt.hist(Hours, bins=24, histtype='bar', edgecolor='black')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Frequency')
    plt.title('Distribution of Hours')
    plt.xticks(range(24))
    plt.show()
    return Hours

def weekly_analysis(data):
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

def calculate_conversion_rates(data, threshold=10):
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
    return attribute_stats, option_stats

def plot_conversion_rates(attribute_stats, option_stats):
    plt.figure(figsize=(12, 6))
    sns.barplot(data=attribute_stats, x='attribute_name', y='conversion_rate', palette='viridis')
    plt.xlabel('Attribute Name')
    plt.ylabel('Conversion Rate (%)')
    plt.title('Conversion Rate by Attribute')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

def funnel_analysis(data):
    grouped_data = data.groupby(['product_id', 'product_name', 'event_type']).size().reset_index(name='count')
    fig = px.funnel(grouped_data, x='count', y='product_name', color='event_type', title='Funnel Analysis of Product Events')
    fig.show()

sheet_name = "Dummy_Data"
sheet_id = "1mIYAIM8DTibovMeV8bvVDO-B9vgwApZTjyxIXXGFGQw"

data = read_and_clean_data(sheet_name, sheet_id)
Hours = time_analysis(data)
weekly_analysis(data)
attribute_stats, option_stats = calculate_conversion_rates(data)
plot_conversion_rates(attribute_stats, option_stats)
