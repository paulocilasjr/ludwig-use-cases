import os
import pandas as pd
from pathlib import Path

def create_ludwig_inputs(samples_df):
    '''
    Create a dataframe with the image paths, labels, and sample name for Ludwig.
    '''
    count = 0
    ludwig_df = pd.DataFrame(columns=['image_path', 'er_status_by_ihc', 'sample'])
    for row in samples_df.itertuples():
        sample_dir = Path(row.filename).stem
        try:
            tiles = os.listdir(os.path.join(sample_dir, sample_dir + '_tiles'))
        except FileNotFoundError:
            print(f'Directory not found for sample: {row.filename}.')
            count += 1
            continue
        # Add each tile to the training data.
        for tile in tiles:
            tile_path = os.path.join(sample_dir, sample_dir + '_tiles', tile)
            ludwig_df.loc[len(ludwig_df)] = {'image_path': tile_path, 'er_status_by_ihc': row.er_status_by_ihc, 'sample': row.sample}
    print(f'Total files not found: {count}')
    return ludwig_df

# Read in samples manifest file.
samples_df = pd.read_csv('er_status_samples.txt', sep='\t')

# Write all data to file.
ludwig_all = create_ludwig_inputs(samples_df)
ludwig_all.to_csv('er_status_all_data.csv', index=False)
