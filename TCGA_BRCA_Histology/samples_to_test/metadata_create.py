import pandas as pd
import os

def process_files(text_file_path, svs_directory, output_csv_path):
    # Load the text file (tab-separated)
    df = pd.read_csv(text_file_path, sep='\t')
    
    # List all .svs files in the specified directory
    svs_files = [f for f in os.listdir(svs_directory) if f.endswith('.svs')]
    
    # Prepare data for the new table
    matched_data = []
    for svs_file in svs_files:
        if svs_file in df['filename'].values:
            # Get the corresponding row from the text file
            row = df[df['filename'] == svs_file].iloc[0]
            sample_name = svs_file
            er_status = row['er_status_by_ihc']
            # Translate er_status_by_ihc to label (Negative -> 0, Positive -> 1)
            label = 1 if er_status == 'Positive' else 0 if er_status == 'Negative' else None
            if label is not None:  # Only include valid labels
                matched_data.append({'sample_name': sample_name, 'label': label})
    
    # Create a DataFrame from the matched data
    result_df = pd.DataFrame(matched_data)
    
    # Save the result to a CSV file
    result_df.to_csv(output_csv_path, index=False)
    print(f"CSV file saved to {output_csv_path}")

# Example usage (update paths as needed)
text_file_path = '60_samples.txt'  # Replace with your text file path
svs_directory = '.'  # Current directory, or replace with your .svs files directory
output_csv_path = 'metadata.csv'  # Output file name
process_files(text_file_path, svs_directory, output_csv_path)
