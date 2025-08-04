import pandas as pd
import re

# Function to extract sample ID (TCGA-XX-XXXX-XX) from sample_name
def extract_sample_id(name):
    match = re.search(r'(TCGA-[A-Z0-9]{2}-[A-Z0-9]{4}-[0-9]{2})', name)
    return match.group(0) if match else None

# Read all files
metadata = pd.read_csv('metadata.csv')
manifest = pd.read_csv('final_TCGA_sample_manifest.csv')
clinical = pd.read_csv('clinical.tsv', sep='\t', low_memory=False)
follow_up = pd.read_csv('follow_up.tsv', sep='\t', low_memory=False)

# Select important columns from manifest, including filename for image_path, discarding er_status_by_ihc, PAM50, and Triple_negative_status to avoid direct leakage
manifest_selected = manifest[['sample', 'filename', 'Histology_Annotation', 'Tumor_or_normal', 'pr_status_by_ihc', 'HER2_status']]

# Select important columns from clinical
clinical_cols = [
    'cases.submitter_id',
    'demographic.age_at_index',
    'demographic.ethnicity',
    'demographic.gender',
    'demographic.race',
    'diagnoses.age_at_diagnosis',
    'diagnoses.ajcc_pathologic_stage',
    'diagnoses.ajcc_pathologic_t',
    'diagnoses.ajcc_pathologic_n',
    'diagnoses.ajcc_pathologic_m',
    'diagnoses.tumor_grade',
    'diagnoses.primary_diagnosis',
    'diagnoses.year_of_diagnosis'
]
clinical_selected = clinical[clinical_cols]

# Group clinical by cases.submitter_id
clinical_grouped = clinical_selected.groupby('cases.submitter_id').first().reset_index()

# Select important columns from follow_up
follow_cols = [
    'cases.submitter_id',
    'other_clinical_attributes.menopause_status',
    'other_clinical_attributes.bmi',
    'other_clinical_attributes.height',
    'other_clinical_attributes.weight',
    'follow_ups.ecog_performance_status',
    'follow_ups.karnofsky_performance_status'
]
follow_selected = follow_up[follow_cols].copy()

# Convert numeric columns in follow_up to numeric, coercing errors to NaN
num_cols = ['other_clinical_attributes.bmi', 'other_clinical_attributes.height', 'other_clinical_attributes.weight']
follow_selected[num_cols] = follow_selected[num_cols].apply(pd.to_numeric, errors='coerce')

# Aggregation for follow_up
cat_cols = ['other_clinical_attributes.menopause_status', 'follow_ups.ecog_performance_status', 'follow_ups.karnofsky_performance_status']
agg_dict = {col: 'mean' for col in num_cols}
agg_dict.update({col: 'first' for col in cat_cols})

follow_grouped = follow_selected.groupby('cases.submitter_id').agg(agg_dict).reset_index()

# List to hold merged data
data_list = []

# Iterate over each row in metadata
for index, row in metadata.iterrows():
    label = row['label']
    sample_id = extract_sample_id(row['sample_name'])
    
    if sample_id is None:
        continue
    
    core = sample_id[:12]
    
    # Create entry with sample_name (core name) and label
    entry = {'sample_name': sample_id, 'label': label}
    
    # Find and add manifest data using sample_id, use filename as image_path
    manifest_row = manifest_selected[manifest_selected['sample'] == sample_id]
    if not manifest_row.empty:
        manifest_dict = manifest_row.iloc[0].to_dict()
        image_path = manifest_dict.pop('filename', '')
        manifest_dict.pop('sample', None)
        entry.update(manifest_dict)
        entry['image_path'] = image_path
    
    # Find and add clinical data using core
    clinical_row = clinical_grouped[clinical_grouped['cases.submitter_id'] == core]
    if not clinical_row.empty:
        clinical_dict = clinical_row.iloc[0].to_dict()
        clinical_dict.pop('cases.submitter_id', None)
        entry.update(clinical_dict)
    
    # Find and add follow_up data using core
    follow_row = follow_grouped[follow_grouped['cases.submitter_id'] == core]
    if not follow_row.empty:
        follow_dict = follow_row.iloc[0].to_dict()
        follow_dict.pop('cases.submitter_id', None)
        entry.update(follow_dict)
    
    data_list.append(entry)

# Create DataFrame from list
merged = pd.DataFrame(data_list)

# Replace "'--" with '' in object columns
object_cols = merged.select_dtypes(include=['object']).columns
merged[object_cols] = merged[object_cols].apply(lambda x: x.str.replace("'--", '') if x.dtype == 'object' else x)

# Drop columns that are entirely blank or NaN
for col in merged.columns:
    if merged[col].dtype == 'object':
        if (merged[col] == '').all():
            merged.drop(col, axis=1, inplace=True)
    else:
        if merged[col].isna().all():
            merged.drop(col, axis=1, inplace=True)

# Save to CSV
merged.to_csv('merged_clinical_data.csv', index=False)

print("Merged CSV file created: merged_clinical_data.csv")
