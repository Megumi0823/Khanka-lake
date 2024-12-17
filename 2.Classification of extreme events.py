import pandas as pd

# Load the clustered data
def load_data(csv_path):
    df = pd.read_csv(csv_path)
    df['date_time'] = pd.to_datetime(df['date_time']) 
    return df

# Calculate the start and end dates of each event
def calculate_event_dates(df):
    event_dates = df.groupby('cluster')['date_time'].agg(['min', 'max']).reset_index()
    event_dates.columns = ['cluster', 'start_date', 'end_date']
    return event_dates

# Determine the type of each event (Drought or Flood) and calculate TWS_anomaly_mean
def determine_event_type_and_anomaly_mean(df):
    event_type = df.groupby('cluster')['TWS_anomaly'].mean().reset_index()
    event_type['event_type'] = event_type['TWS_anomaly'].apply(lambda x: 'Drought' if x < 0 else 'Flood')
    event_type.columns = ['cluster', 'TWS_anomaly_mean', 'event_type']
    return event_type

# Merge event dates and event type
def merge_event_info(event_dates, event_type):
    event_info = pd.merge(event_dates, event_type, on='cluster')
    return event_info

# Save the result to a CSV file
def save_event_info(event_info, output_csv):
    event_info.to_csv(output_csv, index=False)
    print(f"Event information saved to {output_csv}")

# Main function
def main(input_csv, output_csv):
    df = load_data(input_csv)
    
    # Calculate event start and end dates
    event_dates = calculate_event_dates(df)
    
    # Determine event type (Drought or Flood) and calculate TWS_anomaly_mean
    event_type = determine_event_type_and_anomaly_mean(df)
    
    # Merge event dates and type
    event_info = merge_event_info(event_dates, event_type)
    
    save_event_info(event_info, output_csv)

if __name__ == "__main__":
    input_csv = " " # CSV file after clustering with ST-DBSCAN
    output_csv = " "
    
    main(input_csv, output_csv)
