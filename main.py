import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df_tesla = pd.read_csv('TESLA Search Trend vs Price.csv')
df_btc_search = pd.read_csv('Bitcoin Search Trend.csv')
df_btc_price = pd.read_csv('Daily Bitcoin Price.csv')
df_unemployment = pd.read_csv('UE Benefits Search vs UE Rate 2004-19.csv')

#dfs = [df_tesla, df_btc_search, df_btc_price, df_unemployment]

q1 = """ Try to answer these questions about the DataFrames:

    What are the shapes of the DataFrames?
    How many rows & columns do they have?
    What are the column names?
    What is the largest number in the search data column? Try using the .describe() function.
    What is the periodicity of the time series data (daily, weekly, monthly)?
"""
print(q1)
print("Tesla:")

print(df_tesla.shape)
print(df_tesla.head())
print(f"Largest value in TSLA_WEB_SEARCH: {df_tesla.TSLA_WEB_SEARCH.max()}\n")
print(df_tesla.describe())
print("")

print("Unemployment:")
print(df_unemployment.shape)
print(df_unemployment.head())
print(f"Largest value in UE_BENEFITS_WEB_SEARCH: {df_unemployment.UE_BENEFITS_WEB_SEARCH.max()}\n")
print(df_unemployment.describe())
print("")

print("BTC Price")
print(df_btc_price.shape)
print(df_btc_price.head())
print(df_btc_price.describe())
print("")

print("BTC Search")
print(df_btc_search.shape)
print(df_btc_search.head())
print(f"Largest value in BTC_NEWS_SEARCH: {df_btc_search.BTC_NEWS_SEARCH.max()}\n")
print(df_btc_search.describe())
print("")

print("Searching junk data:")
print(f'Missing values for Tesla?: {df_tesla.isna().values.any()}')
print(f'Missing values for U/E?: {df_unemployment.isna().values.any()}')
print(f'Missing values for BTC Search?: {df_btc_search.isna().values.any()}')
print(f'Missing values for BTC Price?: {df_btc_price.isna().values.any()}')
print(f"Number of missing values for BTC price: {df_btc_price.isna().values.sum()}")
print(df_btc_price[df_btc_price.CLOSE.isna()])
df_btc_price.dropna(inplace=True)

#Check one of the dates format
print(type(df_tesla.MONTH[0]))
print(type(df_btc_search.MONTH[0]))
print(type(df_btc_price.DATE[0]))
print(type(df_unemployment.MONTH[0]))

#Convert dates in string format to datetime objects:
df_tesla.MONTH = pd.to_datetime(df_tesla.MONTH)
df_btc_search.MONTH = pd.to_datetime(df_btc_search.MONTH)
df_unemployment.MONTH = pd.to_datetime(df_unemployment.MONTH)
df_btc_price.DATE = pd.to_datetime(df_btc_price.DATE)

#Checking one of them again:
print(type(df_tesla.MONTH[0]))
print(df_tesla.MONTH.head())

#Dimensions of both BTC datasets are different
#Let's use the same time scale to resample the larger one:
df_btc_monthly = df_btc_price.resample('M', on='DATE').last()
print(df_btc_monthly.shape)
print(df_btc_monthly.head())


q2 = """
Plot the Tesla stock price against the Tesla search volume using a line chart and two different axes.
"""
print(q2)
#MONTH  TSLA_WEB_SEARCH  TSLA_USD_CLOSE
plt.figure(figsize=(14,8), dpi=120)
plt.title("Tesla Web Search vs Price", fontsize=18)
plt.xticks(fontsize=14, rotation=45)
ax1 = plt.gca() # get current axes
ax1.set_xlabel('Year', fontsize=14)
ax1.set_ylabel('TSLA Stock Price', color='red', fontsize=14)
ax1.plot(df_tesla.MONTH, df_tesla.TSLA_USD_CLOSE, color='red',
         linewidth=3)
ax1.set_ylim([0, 600])
ax1.set_xlim([df_tesla.MONTH.min(), df_tesla.MONTH.max()])

ax2 = ax1.twinx()
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)
ax2.plot(df_tesla.MONTH, df_tesla.TSLA_WEB_SEARCH, color='skyblue',
         linewidth=3)
#plt.show()
#plt.close()
years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter('%Y')
# format the ticks
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)
plt.show()

#Print BTC chart nicely
print("""
Plot BTC chart looking nicely!
      """)
plt.figure(figsize=(14,8), dpi=120)

plt.title('Bitcoin News Search vs Resampled Price', fontsize=18)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('BTC Price', color='#F08F2E', fontsize=14)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.set_ylim(bottom=0, top=15000)
ax1.set_xlim([df_btc_monthly.index.min(), df_btc_monthly.index.max()])

# Experiment with the linestyle and markers
ax1.plot(df_btc_monthly.index, df_btc_monthly.CLOSE,
         color='#F08F2E', linewidth=3, linestyle='--')
ax2.plot(df_btc_monthly.index, df_btc_search.BTC_NEWS_SEARCH,
         color='skyblue', linewidth=3, marker='o')

plt.show()

# Unemployment
print("""
Plot the search for "unemployment benefits" against the official unemployment rate.
""")
#MONTH  UE_BENEFITS_WEB_SEARCH  UNRATE

plt.figure(figsize=(14,8), dpi=120)

plt.title('Monthly Search of "Unemployment Benefits" in the U.S. vs the unemployement rate', fontsize=18)
plt.xticks(fontsize=14, rotation=45)
plt.yticks(fontsize=14)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('FRED unemployment Rate', color='purple', fontsize=14)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.set_ylim(bottom=3, top=10.5)
ax1.set_xlim([df_unemployment.index.min(), df_unemployment.index.max()])

# Show the grid lines as dark grey lines
ax1.grid(color='grey', linestyle='--')

ax1.plot(df_unemployment.index, df_unemployment.UNRATE,
         color='purple', linewidth=3, linestyle='--')
ax2.plot(df_unemployment.index, df_unemployment.UE_BENEFITS_WEB_SEARCH,
         color='skyblue', linewidth=3, marker='o')

plt.show()

print("""
Calculate the 3-month or 6-month rolling average for the web searches. Plot the 6-month rolling average search data against the actual unemployment. What do you see? Which line moves first?
""")

plt.figure(figsize=(14,8), dpi=120)
plt.title('Rolling Monthly US "Unemployment Benefits" Web Searches vs unemployment rate', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.set_ylabel('FRED unemployment Rate', color='purple', fontsize=16)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=16)

ax1.set_ylim(bottom=3, top=10.5)
ax1.set_xlim([df_unemployment.MONTH[0], df_unemployment.MONTH.max()])

# Calculate the rolling average over a 6 month window
roll_df = df_unemployment[['UE_BENEFITS_WEB_SEARCH', 'UNRATE']].rolling(window=6).mean()

ax1.plot(df_unemployment.MONTH, roll_df.UNRATE, 'purple', linewidth=3, linestyle='-.')
ax2.plot(df_unemployment.MONTH, roll_df.UE_BENEFITS_WEB_SEARCH, 'skyblue', linewidth=3)

plt.show()

#Finantial crisis 2008
print("""
Read the data in the 'UE Benefits Search vs UE Rate 2004-20.csv' into a DataFrame. Convert the MONTH column to Pandas Datetime objects and then plot the chart. What do you see?
""")

df_ue_2020 = pd.read_csv('UE Benefits Search vs UE Rate 2004-20.csv')
df_ue_2020.MONTH = pd.to_datetime(df_ue_2020.MONTH)

plt.figure(figsize=(14,8), dpi=120)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)
plt.title('Monthly US "Unemployment Benefits" Web Search vs unemployment rate incl 2020', fontsize=18)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('FRED unemployment rate', color='purple', fontsize=16)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=16)

ax1.set_xlim([df_ue_2020.MONTH.min(), df_ue_2020.MONTH.max()])

ax1.plot(df_ue_2020.MONTH, df_ue_2020.UNRATE, 'purple', linewidth=3)
ax2.plot(df_ue_2020.MONTH, df_ue_2020.UE_BENEFITS_WEB_SEARCH, 'skyblue', linewidth=3)

plt.show()
