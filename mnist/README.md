TUTORIAL: MNIST database and Ludwig Model

The MNIST dataset is a collection of grayscale images of handwritten digits. The original MNIST database can be found at: https://yann.lecun.com/exdb/mnist/. It consists of four files:
i) training set images; 
ii) training set labels; 
iii) test set images 
iv) test set labels.

The training set contains 60000 examples, and the test set 10000 examples, each image is 28x28 pixels in gray-scale.

Ludwig is an open-source, declarative machine learning framework that makes it easy to define deep learning pipelines with a simple and flexible data-driven configuration system. Ludwig is suitable for a wide variety of AI tasks, and is hosted by the Linux Foundation AI & Data. Ludwig enables you to apply state-of-the-art tabular, natural language processing, and computer vision models to your existing data and put them into production with just a few short commands.

INSTRUCTIONS_TO_ GET_STARTED

# 1. Install Ludwig:

CLI command
$ ```pip install ludwig```

# 2. Download the MNIST dataset: 
To get the MNIST dataset generally follow the Ludwig instructions here: https://ludwig.ai/latest/examples/mnist/. The are two ways to dowload the dataset: CLI or Python script. This tutorial we are going to focus on the CLI command.

CLI command
$ ```ludwig datasets download mnist```

        This command will create a dataset mnist_dataset.csv in the current directory. In addition, there will be directories training/ and testing/ containing the images.

            # Data format
                #column name       # Description
                image_path          file path string for the image
                label               single digit 0 to 9 indicating what digit is shown in the image
                split               integer value indicating a training example (0) or test example (2)

# 3. After downloading the dataset you will need to run ```prepare_dataset.py``` to create the dataset csv file.

CLI command
$python3 prepare_dataset.py

        The script will create a file - mnist_dataset.csv
            # Data format
                # Columns name      # Description
                image_path          file path string for the image
                label               single digit 0 to 9 indicating what digit is shown in the image
                split               integer value indicating a training example (0) or test example (2)

# 4. After running ```prepare_dataset.py```, you can run a ludwig experiment from the command line:

CLI commmand
$ ```ludwig experiment --dataset mnist_dataset.csv   --config config.yaml```
    
        # ludwig experiment command combines the train and evaluation of the model. If you would like to have them separetely:
        ```ludwig train```
        ```ludwig evaluate```

        # The ludwig configuration file describes the machine learning task. This example only uses a small subset of the options povided by Ludwig (https://ludwig.ai/latest/examples/mnist/#download-the-mnist-dataset):
         ```input_features```
         ```output_features```
         ```trainer```

            # config.yaml
            input_features:
            - name: image_path
              type: image
              encoder: 
                  type: stacked_cnn
                  conv_layers:
                    - num_filters: 32
                      filter_size: 3
                      pool_size: 2
                      pool_stride: 2
                    - num_filters: 64
                      filter_size: 3
                      pool_size: 2
                      pool_stride: 2
                      dropout: 0.4
                  fc_layers:
                    - output_size: 128
                      dropout: 0.4

            output_features:
             - name: label
               type: category

            trainer:
              epochs: 5

# 5. To run on Galaxy, create a zip file with the `/training` and `/testing` directories. Then upload the zip file, `mnist_dataset.csv`, and `config.yaml` to Galaxy and run the experiment.
