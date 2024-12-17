import pandas as pd
import math
from datetime import timedelta
from geopy.distance import great_circle
import matplotlib.pyplot as plt

# ST-DBSCAN algorithm
def ST_DBSCAN(df, spatial_threshold, temporal_threshold, min_neighbors):
    cluster_label = 0
    NOISE = -1
    UNMARKED = 777777
    stack = []

    # Initialize the clustering labels for each point as unlabeled
    df['cluster'] = UNMARKED
    
    # Iterate over each point in the dataset
    for index, point in df.iterrows():
        if df.loc[index]['cluster'] == UNMARKED:
            neighborhood = retrieve_neighbors(index, df, spatial_threshold, temporal_threshold)
            
            if len(neighborhood) < min_neighbors:
                df.at[index, 'cluster'] = NOISE  # Marked as noise spot
            else:
                cluster_label += 1
                df.at[index, 'cluster'] = cluster_label  # Marked as a core point

                for neig_index in neighborhood:
                    df.at[neig_index, 'cluster'] = cluster_label
                    stack.append(neig_index)  
                
                while len(stack) > 0:
                    current_point_index = stack.pop()
                    new_neighborhood = retrieve_neighbors(current_point_index, df, spatial_threshold, temporal_threshold)
                    
                    if len(new_neighborhood) >= min_neighbors:
                        for neig_index in new_neighborhood:
                            neig_cluster = df.loc[neig_index]['cluster']
                            if (neig_cluster != NOISE) & (neig_cluster == UNMARKED):
                                df.at[neig_index, 'cluster'] = cluster_label
                                stack.append(neig_index)
    return df

# Get Neighborhood Points
def retrieve_neighbors(index_center, df, spatial_threshold, temporal_threshold):
    neighborhood = []
    center_point = df.loc[index_center]

    # Filtering Neighborhoods by Time
    min_time = center_point['date_time'] - timedelta(days=temporal_threshold)
    max_time = center_point['date_time'] + timedelta(days=temporal_threshold)
    df_time_filtered = df[(df['date_time'] >= min_time) & (df['date_time'] <= max_time)]

    # Filter Neighborhoods by Distance
    for index, point in df_time_filtered.iterrows():
        if index != index_center:
            distance = great_circle((center_point['lat'], center_point['lon']), (point['lat'], point['lon'])).meters
            if distance <= spatial_threshold:
                neighborhood.append(index)

    return neighborhood

def load_and_prepare_data(csv_path):
    df = pd.read_csv(csv_path)

    # Conversion of data to long form suitable for ST-DBSCAN format
    df_melted = pd.melt(df, id_vars=['lon', 'lat'], var_name='date_time', value_name='TWS_anomaly')
    df_melted['date_time'] = pd.to_datetime(df_melted['date_time'], format='%Y-%m')

    return df_melted

# Visualization of clustering results
def plot_clusters(df_clustered):
    plt.figure(figsize=(10, 6))

    clusters = df_clustered['cluster'].unique()
    colors = plt.cm.get_cmap('tab10', len(clusters))

    for i, cluster in enumerate(clusters):
        cluster_data = df_clustered[df_clustered['cluster'] == cluster]
        plt.scatter(cluster_data['lon'], cluster_data['lat'], 
                    color=colors(i), label=f'Cluster {cluster}' if cluster != -1 else 'Noise', s=10)

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Cluster Visualization of TWS Anomalies')
    plt.legend(loc='best', markerscale=3)
    plt.grid(True)
    plt.show()

# Save the clustering results as a CSV file
def save_cluster_results(df_clustered, output_path):
    df_clustered.to_csv(output_path, index=False)
    print(f"Cluster results saved to {output_path}")

# Main function
def main(csv_path, output_csv):
    df_melted = load_and_prepare_data(csv_path)

    # Setting parameters
    spatial_threshold = 250   # For example:250 kilometer
    temporal_threshold = 30    # For example: 30 days
    min_neighbors = 3          # For example: At least 3 neighbors

    # Running the ST-DBSCAN algorithm
    df_clustered = ST_DBSCAN(df_melted, spatial_threshold, temporal_threshold, min_neighbors)

    save_cluster_results(df_clustered, output_csv)

    plot_clusters(df_clustered)

if __name__ == "__main__":
    input_csv = " " # CSV file for TWSA
    output_csv = " "
    main(input_csv, output_csv)
