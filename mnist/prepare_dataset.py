# Adapted from https://ludwig.ai/0.4/examples/mnist/ to create mnist.csv because dataset download does not create mnist.csv

import os

with open('mnist_dataset.csv', 'w') as output_file:
    output_file.write('image_path,label,split\n')
    for name in ['training', 'testing']:
        print('=== creating {} dataset rows ==='.format(name))
        split = 0 if name == 'training' else 2
        for i in range(10):
            path = '{}/{}'.format(name, i)
            for file in os.listdir(path):
                if file.endswith(".png"):
                    output_file.write('{},{},{}\n'.format(os.path.join(path, file), str(i), split))