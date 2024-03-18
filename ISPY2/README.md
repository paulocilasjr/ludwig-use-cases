# Ludwig-ISPY2

## Paper
- https://www.cell.com/cancer-cell/fulltext/S1535-6108(22)00216-1 

## Steps for running a Ludwig experiment:

1. Download and prepare the data: `make download-and-prepare-data` This will create two files, `ispy2_phenotype.tsv` and `ispy2_expression_std_sorted.tsv`
1. Run Ludwig experiment: `make ludwig-experiment`. This will (1) create the needed configuration file for Ludwig; (2) prepare the data for the experiment by scaling it and combining the X and Y matrices; (3) run Ludwig on the prepared data using the configuration file.
