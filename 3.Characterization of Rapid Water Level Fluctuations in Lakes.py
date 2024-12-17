import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import LinearSegmentedColormap

# Read data
file_path = ' '  
df = pd.read_csv(file_path)

# Data preprocessing
df['start_date'] = pd.to_datetime(df['start_date'])
df['end_date'] = pd.to_datetime(df['end_date'])
df['duration'] = (df['end_date'] - df['start_date']).dt.days

# Check lake level change L-value
print(df['L'].describe())

# # Defining color gradients
# colors = [" ", " "]
# cmap = LinearSegmentedColormap.from_list(" ", colors)

# # Normalizing lake change L-values for color intensity
# norm = plt.Normalize(0, 1)

plt.rcParams['font.family'] = 'Times New Roman'

# # Creating Charts
# plt.figure(figsize=(10, 3))
# scatter = plt.scatter(df['start_date'], df['L'], 
#                       s=(df['duration'] * 10),  # The size of the circle represents the duration of the event
#                       c=df['TWS_anomaly_mean'],  # Color intensities represent anomalous means
#                       cmap=cmap, norm=norm, alpha=0.7, marker='o')  

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator())

plt.ylim(0, 1)
plt.gca().yaxis.set_ticks([])

# # Add a color bar to indicate
# cbar = plt.colorbar(scatter, label='')
# cbar.set_ticks([, , ])

plt.tight_layout()
plt.show()