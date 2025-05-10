#!/bin/bash
#SBATCH --job-name=ludwig_experiment     # Job name
#SBATCH --output=ludwig_experiment.out  # Output file
#SBATCH --error=ludwig_experiment.err   # Error file
#SBATCH --ntasks=1                      # Number of tasks
#SBATCH --cpus-per-task=50              # Number of CPU cores
#SBATCH --mem=500G                      # Memory allocation
#SBATCH --gres=gpu:1                    # Request 1 GPU
#SBATCH --time=3-02:00:00               # Time limit (days-HH:MM:SS)

# Initialize Conda environment
eval "$(conda shell.bash hook)"
conda activate ludwig

# Reinstall bitsandbytes if necessary
pip install bitsandbytes --upgrade --no-cache-dir
# Run the Ludwig experiment
ludwig experiment --dataset er_status_all_data.csv --config config.yaml --output_directory ludwig_output 
