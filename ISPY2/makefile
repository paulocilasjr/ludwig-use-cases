DATA_DIRECTORY = .
DRUG = Paclitaxel+Pembrolizumab
SCALED_DATASET = $(DRUG)_scaled_dataset.tsv
BASE_CONFIG = base_config.yaml

# Download and prepare raw dataset.
download-and-prepare-data:
	curl -L ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE194nnn/GSE194040/suppl/GSE194040_ISPY2ResID_AgilentGeneExp_990_FrshFrzn_meanCol_geneLevel_n988.txt.gz -O
	gunzip GSE194040_ISPY2ResID_AgilentGeneExp_990_FrshFrzn_meanCol_geneLevel_n988.txt.gz
	python download_and_prepare_ispy2_data.py

# Create scaled dataset.
$(SCALED_DATASET):
	python prepare_data.py "$(DATA_DIRECTORY)/ispy2_expression_std_sorted.tsv" "$(DATA_DIRECTORY)/ispy2_phenotype.tsv" $(DRUG) $(SCALED_DATASET)

# Create final configuration file.
$(DRUG)_final_config.yaml: create_input_features.py base_config.yaml $(SCALED_DATASET)
	python create_input_features.py "$(SCALED_DATASET)" $(DRUG)_final_config.yaml $(BASE_CONFIG)

# Run a ludwig experiment using the scaled dataset. Results are placed into the $(DRUG) directory.
ludwig-experiment: $(DRUG)_final_config.yaml $(SCALED_DATASET)
	mkdir -p $(DRUG) && pushd $(DRUG) && /usr/bin/time ludwig experiment --dataset ../$(SCALED_DATASET) -c ../$(DRUG)_final_config.yaml -rs 456

clean:
	rm *final_config.yaml *_scaled_dataset.*


