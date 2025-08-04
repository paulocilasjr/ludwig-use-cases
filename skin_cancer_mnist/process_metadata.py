import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Read the metadata CSV file
csv_path = "HAM10000_metadata.csv"  # Adjust path if needed
df = pd.read_csv(csv_path)

# Verify required columns exist
required_cols = ['image_id', 'dx']
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Column '{col}' not found in the CSV file")

# Define label mapping based on HAM10000 'dx' values
label_mapping = {
    'akiec': 0,  # Actinic Keratosis / Intraepithelial Carcinoma
    'bcc': 1,    # Basal Cell Carcinoma
    'bkl': 2,    # Benign Keratosis-like Lesions
    'df': 3,     # Dermatofibroma
    'mel': 6,    # Melanoma (note: 'mel' comes after 'nv' in your list)
    'nv': 4,     # Melanocytic Nevus
    'vasc': 5    # Vascular Lesions
}

# Validate 'dx' values
unique_dx = df['dx'].unique()
if not set(unique_dx).issubset(label_mapping.keys()):
    raise ValueError(f"Unexpected 'dx' values found: {unique_dx}. Expected {list(label_mapping.keys())}")

print("unique_dx")
# Create new DataFrame with required columns
new_df = pd.DataFrame()
new_df['image_id'] = df['image_id'] + '.jpg'  # Append .jpg extension
new_df['label'] = df['dx'].map(label_mapping)  # Map dx to numerical labels

# Initialize 'split' column
new_df['split'] = None

# Define split proportions
train_fraction = 0.7  # 70% for training ("0")
test_fraction = 0.3   # 30% for testing ("2")

# Process each label separately
unique_labels = new_df['label'].unique()
for label in unique_labels:
    # Filter rows for the current label
    label_df = new_df[new_df['label'] == label]
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
    new_df.loc[train_indices, 'split'] = "0"  # Training
    new_df.loc[test_indices, 'split'] = "2"   # Test

# Verify no unassigned splits remain
if new_df['split'].isnull().any():
    raise ValueError("Some samples were not assigned a split")

# Save the new DataFrame
output_csv = "ham10000_split.csv"
new_df.to_csv(output_csv, index=False)
print(f"New CSV with 'image_id', 'label', and 'split' saved to: {output_csv}")

# Summary of split counts per label
print("\nSplit counts per label:")
dx_label_map = {v: k for k, v in label_mapping.items()}  # Reverse mapping for display
for label in sorted(unique_labels):
    label_counts = new_df[new_df['label'] == label]['split'].value_counts()
    dx_name = dx_label_map[label]
    print(f"Label {label} ({dx_name}): Train (0): {label_counts.get('0', 0)}, Test (2): {label_counts.get('2', 0)}")
