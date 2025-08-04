import sys
import pandas as pd
from datetime import datetime
import argparse  # Import the argparse module

# Set up argument parsing
parser = argparse.ArgumentParser(description="Sample manifest file.")
parser.add_argument("--sample_manifest", required=True, help="Path to the sample manifest file")
parser.add_argument("--number_samples", required=True, type=int, help="Number of samples to extract")
args = parser.parse_args()

# Use the arguments
manifest_file = args.sample_manifest
N = args.number_samples

# Read manifest file.
df = pd.read_csv(manifest_file, sep='\t')

# Sample positive, negative from er_status_by_ihc column and write to file.
er_df = df[df['er_status_by_ihc'].isin(['Positive', 'Negative'])].drop_duplicates(subset=['sample']) # Exclude Duplicates in sample column

# Check if the number of samples requested is greater than the number of unique samples in each group.
group_counts = er_df.groupby('er_status_by_ihc').size()
for group, count in group_counts.items():
    if N > count:
        print(f"Warning: Cannot sample {N} from group '{group}'.  Setting sample size to {count}.")
        N = count # Adjust N to the maximum possible value

er_df_sample = er_df.groupby('er_status_by_ihc').sample(n=N, random_state=1)

# Get the current date in MMDDYY format
date_str = datetime.now().strftime('%m%d%y')
output_filename = f'er_status_samples_{date_str}.txt'  # create the filename

er_df_sample.to_csv(output_filename, sep='\t', index=False)