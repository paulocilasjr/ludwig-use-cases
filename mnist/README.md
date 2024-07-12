1. Generally follow the Ludwig instructions here: https://ludwig.ai/latest/examples/mnist/, but after downloading the dataset, you will need to run ```prepare_dataset.py``` to create the dataset csv.

2. After running ```prepare_dataset.py```, you can run a ludwig experiment from the command line:
```ludwig experiment --dataset mnist_dataset.csv   --config config.yaml```

3. To run on Galaxy, create a zip file with the `/training` and `/testing` directories. Then upload the zip file, `mnist_dataset.csv`, and `config.yaml` to Galaxy and run the experiment.

