import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Read the CSV file
csv_path = "hmnist_28_28_RGB.csv"  # Adjust path if needed
df = pd.read_csv(csv_path)

# Verify the 'label' column exists and contains expected values (0-6)
if 'label' not in df.columns:
    raise ValueError("Column 'label' not found in the CSV file")
unique_labels = df['label'].unique()
expected_labels = set(range(7))  # 0 to 6
if not set(unique_labels).issubset(expected_labels):
    raise ValueError(f"Unexpected labels found: {unique_labels}. Expected 0-6")

# Identify pixel columns
pixel_cols = [col for col in df.columns if col.startswith('pixel')]
num_pixels = len(pixel_cols)

# Check if number of pixels matches an RGB image (divisible by 3)
if num_pixels % 3 != 0:
    raise ValueError(f"Number of pixel columns ({num_pixels}) is not divisible by 3 for RGB")
channels = 3
pixels_per_channel = num_pixels // channels
height = width = int((pixels_per_channel) ** 0.5)  # Assume square image
if height * width * channels != num_pixels:
    raise ValueError(f"Cannot reshape {num_pixels} pixels into a square RGB image")

print(f"Detected image size: {height}x{width}x{channels} ({num_pixels} pixels)")

# Transform pixel columns into a single space-separated string column
df['image'] = df[pixel_cols].apply(lambda row: ' '.join(map(str, row)), axis=1)

# Drop the original pixel columns
df = df.drop(columns=pixel_cols)

# Initialize the 'split' column with a default value
df['split'] = None

# Define split proportions
train_fraction = 0.7  # 70% for training ("0")
test_fraction = 0.3   # 30% for testing ("2")

# Process each label separately
for label in unique_labels:
    # Filter rows for the current label
    label_df = df[df['label'] == label]
    num_samples = len(label_df)

    # Calculate number of samples for each split
    num_train = int(round(num_samples * train_fraction))  # 70%
    num_test = num_samples - num_train                    # Remaining 30%

    # Shuffle indices for random assignment
    indices = label_df.index.to_numpy()
    np.random.shuffle(indices)

    # Assign splits
    train_indices = indices[:num_train]
    test_indices = indices[num_train:num_train + num_test]

    # Verify all samples are covered
    if len(train_indices) + len(test_indices) != num_samples:
        raise ValueError(f"Label {label}: Split mismatch. Train: {len(train_indices)}, Test: {len(test_indices)}, Total: {num_samples}")

    # Set split values
    df.loc[train_indices, 'split'] = "0"  # Training
    df.loc[test_indices, 'split'] = "2"   # Test

# Verify no unassigned splits remain
if df['split'].isnull().any():
    raise ValueError("Some samples were not assigned a split")

# Save the updated DataFrame
output_csv = "hmnist_28_28_RGB_split.csv"
df.to_csv(output_csv, index=False)
print(f"Updated CSV with 'split' and 'image' columns saved to: {output_csv}")

# Summary of split counts per label
print("\nSplit counts per label:")
for label in sorted(unique_labels):
    label_counts = df[df['label'] == label]['split'].value_counts()
    print(f"Label {label}: Train (0): {label_counts.get('0', 0)}, Test (2): {label_counts.get('2', 0)}")
