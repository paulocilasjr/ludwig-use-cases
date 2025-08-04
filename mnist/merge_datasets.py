import pandas as pd
import argparse
import numpy as np

def process_vectors(df, vector_columns):
    """
    Ensures all vectors are the same size by padding with zeros and converts them to whitespace-separated strings.
    
    Args:
        df (pd.DataFrame): DataFrame containing vector columns.
        vector_columns (list): List of vector column names.
        
    Returns:
        pd.Series: Processed vector column with whitespace-separated values.
    """
    # Determine the maximum vector size
    max_size = max(df[vector_columns].notna().sum(axis=1))

    # Fill NaNs with 0 and ensure consistent vector length
    df[vector_columns] = df[vector_columns].apply(pd.to_numeric, errors='coerce').fillna(0)

    # Convert rows into whitespace-separated strings
    df["embedding"] = df[vector_columns].apply(lambda row: " ".join(map(str, row[:max_size])), axis=1)

    # Drop original vector columns
    df = df.drop(columns=vector_columns)

    return df

def merge_csv_files(metadata_file, embeddings_file, output_file):
    """
    Merges two CSV files on the 'sample_name' column, processes vector embeddings,
    and saves the result to a new CSV file.
    """
    # Load the CSV files
    df_metadata = pd.read_csv(metadata_file)
    df_embeddings = pd.read_csv(embeddings_file)
    
    # Identify vector columns (assumes they start with "vector")
    vector_columns = [col for col in df_embeddings.columns if col.startswith("vector")]

    # Process the vector embeddings
    df_embeddings = process_vectors(df_embeddings, vector_columns)
    
    # Merge on 'sample_name'
    df_merged = pd.merge(df_metadata, df_embeddings, on='sample_name', how='inner')
    
    # Save to new CSV file
    df_merged.to_csv(output_file, index=False)
    print(f"Merged file saved as {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge two CSV files on 'sample_name' column, process vector embeddings, and save the output.")
    parser.add_argument("metadata_file", type=str, help="Path to mnist_embedding_metadata.csv")
    parser.add_argument("embeddings_file", type=str, help="Path to mnist_embeddings.csv")
    parser.add_argument("output_file", type=str, help="Path to save the merged CSV file")
    
    args = parser.parse_args()
    
    merge_csv_files(args.metadata_file, args.embeddings_file, args.output_file)
