import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# --- 1. Synthetic Data Generation ---
np.random.seed(42) # for reproducibility
# Number of menu items and days
num_items = 5
num_days = 100
# Generate synthetic data
dates = pd.to_datetime(pd.date_range(start='2023-01-01', periods=num_days))
items = [f'Item {i+1}' for i in range(num_items)]
data = {'Date': []}
for item in items:
    data[item + '_Rating'] = np.random.normal(loc=4, scale=1, size=num_days).clip(1, 5) # ratings 1-5
    data[item + '_Reviews'] = np.random.randint(1, 50, size=num_days) # number of reviews
    data['Date'].extend(dates)
df = pd.DataFrame(data)
df = df.sort_values('Date')
df = df.reset_index(drop=True)
df['Overall_Rating'] = df[[col for col in df.columns if '_Rating' in col]].mean(axis=1)
# --- 2. Data Cleaning and Feature Engineering ---
# (No significant cleaning needed for synthetic data)
df['Rating_Volatility'] = df['Overall_Rating'].rolling(window=7).std() # 7-day rolling standard deviation of overall rating
# --- 3. Analysis ---
# Calculate correlation between item ratings and overall rating volatility
correlations = df[[col for col in df.columns if '_Rating' in col] + ['Rating_Volatility']].corr()['Rating_Volatility'][:-1]
# Identify items with high correlation (positive or negative)
high_impact_items = correlations[abs(correlations) > 0.3]
# --- 4. Visualization ---
plt.figure(figsize=(12, 6))
sns.barplot(x=high_impact_items.index, y=high_impact_items.values)
plt.title('Correlation between Item Ratings and Overall Rating Volatility')
plt.xlabel('Menu Item')
plt.ylabel('Correlation')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
# Save the plot to a file
output_filename = 'item_rating_volatility_correlation.png'
plt.savefig(output_filename)
print(f"Plot saved to {output_filename}")
# --- 5.  Further Analysis (Optional) ---
#  Could perform time series analysis on individual item ratings to identify trends and seasonality.
#  Could incorporate review sentiment analysis (requires additional libraries and data).
print("\nItems with high impact on rating volatility:")
print(high_impact_items)