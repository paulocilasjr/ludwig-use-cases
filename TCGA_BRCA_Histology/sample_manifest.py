import sys
import pandas as pd

# TODO: make argument parsing more robust.
if len(sys.argv) != 2:
    print('Usage: python sample_manifest.py <N>')
    sys.exit(1)
N = int(sys.argv[1])

# Read manifest file.
df = pd.read_csv('final_TCGA_sample_manifest.txt', sep='\t')

# Sample positive, negative from er_status_by_ihc column and write to file.
er_df = df[df['er_status_by_ihc'].isin(['Positive', 'Negative'])]
er_df_sample = er_df.groupby('er_status_by_ihc').sample(n=N, random_state=1)
er_df_sample.to_csv('er_status_samples.txt', sep='\t', index=False)