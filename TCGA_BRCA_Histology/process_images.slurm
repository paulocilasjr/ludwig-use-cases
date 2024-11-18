#!/bin/bash
#SBATCH --job-name=process_images
#SBATCH --cpus-per-task=1
#SBATCH --mem=10G
#SBATCH --array=0-19
#SBATCH --gres gpu:a30:1      # select one A30 GPU per task / node

batches=(./batch_files/batch_aa batch_ab batch_ac batch_ad batch_ae batch_af batch_ag batch_ah batch_ai batch_aj \
         batch_ak batch_al batch_am batch_an batch_ao batch_ap batch_aq batch_ar batch_as batch_at)

# Prepending './batch_files/' to each batch entry
for i in "${!batches[@]}"; do
    batches[$i]="./batch_files/${batches[$i]}"
done

# Fetch the batch corresponding to the SLURM_ARRAY_TASK_ID
batch=${batches[$SLURM_ARRAY_TASK_ID]}

# Execute the script with the selected batch
bash tile_slides.sh $batch
