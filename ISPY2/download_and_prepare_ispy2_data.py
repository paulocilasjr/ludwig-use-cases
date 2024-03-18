import GEOparse
import pandas as pd

#
#
# Download and prepare the ISPY2 phenotypic and gene expression datasets. Script will create two files in the current directory
# - ispy2_phenotype.tsv : this is a TSV with three columns: ISPY ID, PCR or no, trial arm
# - ispy2_expression_std_sorted.tsv : this is a TSV where rows are patients and columns are genes. 
# Rows are sorted by patient ID and columns are sorted by standard deviation.
#
#

#
# Prepare the phenotype data: output is a dataframe with three columns: ISPY ID, PCR or no, trial arm.
# 

# Download the GEO entry.
gse = GEOparse.get_GEO("GSE196096")

# Get the phenotype data.
pheno_df = gse.phenotype_data

# Remove 'ISPY2' in front of identifiers.
pheno_df['title'] = pheno_df['title'].str.split('_').str[-1]

# Filter the phenotype data to create a dataframe with three columns: ISPY ID, PCR or no, trial arm.
filtered_df = pheno_df[~(pheno_df['characteristics_ch1.6.arm'].isna())].filter(regex='title|arm|pcr', axis=1)
filtered_df = filtered_df[['title', 'characteristics_ch1.5.pcr', 'characteristics_ch1.6.arm']]
filtered_df.columns = ['Patient', 'PCR', 'Arm']
filtered_df['Arm'] = filtered_df['Arm'].str.replace(' ', '')
filtered_df.to_csv('./ispy2_phenotype.tsv', sep='\t', index=False)

#
# Prepare the gene expression data: output is a dataframe where rows are patients and columns are genes. 
# Rows are sorted by patient ID and columns are sorted by standard deviation.
# 
GENE_EXPRESSION_FILE = 'GSE194040_ISPY2ResID_AgilentGeneExp_990_FrshFrzn_meanCol_geneLevel_n988.txt'
expression_df = pd.read_csv(GENE_EXPRESSION_FILE, sep='\t').sort_index().T.sort_index()
expression_df = expression_df.reindex(expression_df.std().sort_values(ascending=False).index, axis=1)
expression_df.to_csv('./ispy2_expression_std_sorted.tsv', sep='\t')
