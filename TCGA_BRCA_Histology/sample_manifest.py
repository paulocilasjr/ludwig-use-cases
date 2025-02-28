import sys
import pandas as pd

# Read manifest file
df = pd.read_csv('final_TCGA_sample_manifest.txt', sep='\t')

# Filter for Positive and Negative values in er_status_by_ihc
er_df = df[df['er_status_by_ihc'].isin(['Positive', 'Negative'])]

# Check if an argument is provided
if len(sys.argv) == 2:
    try:
        N = int(sys.argv[1])
        er_df_sample = er_df.groupby('er_status_by_ihc').sample(n=N, random_state=1)
    except ValueError:
        print('Error: Argument must be an integer.')
        sys.exit(1)
except (ValueError, IndexError):
    er_df_sample = er_df  # Use all available rows if no valid argument is given

# Write output to file
er_df_sample.to_csv('er_status_samples.txt', sep='\t', index=False)
