# TUTORIAL: MNIST database and Ludwig Model

The MNIST dataset is a collection of grayscale images of handwritten digits. The original MNIST database can be found at: https://yann.lecun.com/exdb/mnist/. It consists of four files:
i) training set images; 
ii) training set labels; 
iii) test set images 
iv) test set labels.

The training set contains 60000 examples, and the test set 10000 examples, each image is 28x28 pixels in gray-scale.

Ludwig is an open-source, declarative machine learning framework that makes it easy to define deep learning pipelines with a simple and flexible data-driven configuration system. Ludwig is suitable for a wide variety of AI tasks, and is hosted by the Linux Foundation AI & Data. Ludwig enables you to apply state-of-the-art tabular, natural language processing, and computer vision models to your existing data and put them into production with just a few short commands.

# INSTRUCTIONS TO GET STARTED

## 1. Install Ludwig:

CLI command
$ ```pip install ludwig```

## 2. Download the MNIST dataset: 
To get the MNIST dataset generally follow the Ludwig instructions here: https://ludwig.ai/latest/examples/mnist/. The are two ways to dowload the dataset: CLI or Python script. This tutorial we are going to focus on the CLI command.

CLI command
$ ```ludwig datasets download mnist```

        This command will create a dataset mnist_dataset.csv in the current directory. In addition, there will be directories training/ and testing/ containing the images.

            # Data format
                #column name       # Description
                image_path          file path string for the image
                label               single digit 0 to 9 indicating what digit is shown in the image
                split               integer value indicating a training example (0) or test example (2)

## 3. After downloading 

Run ```prepare_dataset.py``` to create the dataset csv file.

CLI command
$python3 prepare_dataset.py

        The script will create a file - mnist_dataset.csv
            # Data format
                # Columns name      # Description
                image_path          file path string for the image
                label               single digit 0 to 9 indicating what digit is shown in the image
                split               integer value indicating a training example (0) or test example (2)

## 4. Run a ludwig experiment 

Run Ludwig Experiment:

CLI commmand
$ ```ludwig experiment --dataset mnist_dataset.csv   --config config.yaml```

## 5. Run on Galaxy

Create a zip file with the `/training` and `/testing` directories. Then upload the zip file, `mnist_dataset.csv`, and `config.yaml` to Galaxy and run the experiment.
