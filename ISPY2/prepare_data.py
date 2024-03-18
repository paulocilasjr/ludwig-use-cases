'''
Prepare data for use in Ludwig.
'''

import pandas as pd
import argparse
from sklearn.preprocessing import MinMaxScaler

if __name__ == "__main__":
    # Argument parsing.
    parser = argparse.ArgumentParser()
    parser.add_argument("x_matrix_file", help="X_matrix file")
    parser.add_argument("y_matrix_file", help="Y_matrix file")
    parser.add_argument("drug", help="Drug to use for filtering")
    parser.add_argument("output_matrix_file", help="Output matrix file")
    args = parser.parse_args()
    x_matrix_file = args.x_matrix_file
    y_matrix_file = args.y_matrix_file
    output_matrix_file = args.output_matrix_file
    drug = args.drug
    
    # Read X, Y matrics.
    x_df = pd.read_csv(x_matrix_file, delimiter="\t", header=0, index_col=0)
    y_df = pd.read_csv(y_matrix_file, delimiter="\t", header=0, index_col=0)

    #
    # Process X matrix.
    #

    # Rename patient ID column in X matrix and select for 7k genes.
    x_df.index.name = "Patient"

    # TODO: (1) Make this a parameter and (2) note that this only works if using a matrix sorted by STD/MAD.
    N = 7000
    x_df = x_df.iloc[:, 0:N]
    # Set min-max range to [0,1] in X matrix columns and write out combined matrix.
    scaler = MinMaxScaler()
    x_df[x_df.columns] = scaler.fit_transform(x_df)
    x_df

    # 
    # Process Y matrix.
    # 

    y_df = y_df[y_df['Arm'] == drug]
    
    #
    # Join X and Y matrices and write result to file.
    #
    x_df.index = x_df.index.astype('str')
    y_df.index = y_df.index.astype('str')
    joined_df = x_df.join(y_df, how="inner")
    joined_df = joined_df.drop('Arm', axis=1)
    joined_df.to_csv(output_matrix_file, sep="\t", index=False)
