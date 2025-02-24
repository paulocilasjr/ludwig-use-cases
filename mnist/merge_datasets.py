import pandas as pd
import argparse

def merge_csv_files(metadata_file, embeddings_file, output_file):
    # Load the CSV files
    df_metadata = pd.read_csv(metadata_file)
    df_embeddings = pd.read_csv(embeddings_file)
    
    # Merge on 'sample_name'
    df_merged = pd.merge(df_metadata, df_embeddings, on='sample_name', how='inner')
    
    # Save to new CSV file
    df_merged.to_csv(output_file, index=False)
    print(f"Merged file saved as {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge two CSV files on 'sample_name' column.")
    parser.add_argument("metadata_file", type=str, help="Path to mnist_embedding_metadata.csv")
    parser.add_argument("embeddings_file", type=str, help="Path to mnist_embeddings.csv")
    parser.add_argument("output_file", type=str, help="Path to save the merged CSV file")
    
    args = parser.parse_args()
    
    merge_csv_files(args.metadata_file, args.embeddings_file, args.output_file)