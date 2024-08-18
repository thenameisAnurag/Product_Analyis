### README

#### Overview
This script performs various data analyses and visualizations on data extracted from a Google Sheets document. It includes functions for reading and cleaning data, analyzing time distributions, evaluating weekly engagement, calculating conversion rates, and performing funnel analysis.

#### Requirements
- Python 3.x
- Libraries: `pandas`, `seaborn`, `matplotlib`, `numpy`, `plotly`

You can install the required libraries using:
```bash
pip install pandas seaborn matplotlib numpy plotly
```

#### How to Run
1. **Save the Script**: Save the Python script as `data_analysis.py`.

2. **Update Google Sheets Information**:
   - Replace `sheet_name` with the name of the sheet in your Google Sheets document.
   - Replace `sheet_id` with the ID of your Google Sheets document. 

3. **Execute the Script**: Open your terminal or command prompt and run the script using:
   ```bash
   python data_analysis.py
   ```

4. **View Output**: The script will generate several visualizations, including:
   - **Distribution of Hours**: A histogram showing the distribution of hours.
   - **User Engagement by Day of the Week**: Line plots of average time spent on attributes and options by day of the week.
   - **Conversion Rate by Attribute**: A bar plot showing the conversion rates by attribute.
   - **Funnel Analysis of Product Events**: A funnel chart visualizing the product event stages.

#### Script Functions
- **`read_and_clean_data(sheet_name, sheet_id)`**: Reads data from a Google Sheets document, cleans it by dropping empty rows and columns, and formats the timestamp.
- **`time_analysis(data)`**: Analyzes the distribution of hours in the dataset and visualizes it using a histogram.
- **`weekly_analysis(data)`**: Analyzes user engagement by day of the week and plots average time spent on attributes and options.
- **`calculate_conversion_rates(data, threshold=10)`**: Calculates conversion rates based on a threshold for time spent on options. Returns statistics for attributes and options.
- **`plot_conversion_rates(attribute_stats, option_stats)`**: Plots conversion rates by attribute using a bar chart.
- **`funnel_analysis(data)`**: Performs funnel analysis of product events and visualizes it using a funnel chart.

#### Assumptions
- The Google Sheets data must include columns such as `timestamp`, `time_spend_on_att`, `option_time_spend`, `attribute_name`, `attribute_id`, `option_name`, `option_id`, `product_id`, `product_name`, and `event_type`.
- The `timestamp` column is assumed to be in a format that can be converted to datetime.

#### Limitations
- **Data Format**: The script assumes a specific data format and column names. If the data format changes, the script may need to be updated.
- **Missing Data**: If the dataset has missing or incorrect values, it might affect the analysis results.

Make sure to review and adapt the script according to your specific data and requirements.
