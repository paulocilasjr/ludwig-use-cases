1. Use subsample notebook to get a sample of all TCGA samples:
    ```
    python sample_manifest.py 10
    ```

    This will create a file called `er_status_samples.txt` with 10 samples from each class.
2. Download files using gdc_client or copy files using script:
    ```
    gdc-client download -m er_status_samples.txt
    ```
3. Tile images using script.
4. Create Ludwig dataset using prepare_ludwig_training_file notebook
5. Run Ludwig
6. Visualize results. Some useful commands:
    ludwig visualize --visualization roc_curves_from_test_statistics \
                  --test_statistics results/experiment_run_3/test_statistics.json \
                  --output_directory visualizations \
                  --file_format png --output_feature_name er_status_by_ihc

    ludwig visualize --visualization confusion_matrix \
                  --ground_truth_metadata results/experiment_run_3/model/training_set_metadata.json \
                  --output_directory visualizations \
                  --file_format png --test_statistics results/experiment_run_3/test_statistics.json
                  