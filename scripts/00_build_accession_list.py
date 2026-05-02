# ============================================================
# SCRIPT 0: BUILD GCA ACCESSION LIST FROM RAW METADATA
# ============================================================
# Author: Y. Lakshmi Sai Varshini
# Institution: SRM Institute of Science and Technology
# Supervisor: Dr. P. Rathinasabapathi
#
# Purpose:
#   Takes raw metadata CSV files downloaded from BV-BRC and NCBI
#   and produces:
#   - gca_accessions_final.txt  : 281 valid GCA accessions for download
#   - wgs_accessions.txt        : 71 WGS format accessions (excluded)
#   - batch1.txt to batch4.txt  : GCA accessions split into 4 batches
#
# Run this script AFTER downloading metadata files manually
# (see docs/01_database_download_guide.md)
#
# Run this script BEFORE downloading FASTA files
# (see scripts/01_download_genomes.sh)
#
# Requirements:
#   pip install pandas openpyxl
#
# Usage:
#   python scripts/00_build_accession_list.py
# ============================================================

import pandas as pd
import re
import os
import math

# ── File paths ───────────────────────────────────────────────
BVBRC_DIR  = 'data/metadata/bvbrc'
NCBI_DIR   = 'data/metadata/ncbi'
OUTPUT_DIR = 'data/accessions'

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Step 1: Load BV-BRC metadata (all 4 countries) ───────────
print("Loading BV-BRC metadata...")
bvbrc_files = [
    os.path.join(BVBRC_DIR, 'BVBRC_India_Metadata.csv'),
    os.path.join(BVBRC_DIR, 'BVBRC_Pakistan_Metadata.csv'),
    os.path.join(BVBRC_DIR, 'BVBRC_Bangladesh_Metadata.csv'),
    os.path.join(BVBRC_DIR, 'BVBRC_Nepal_Metadata.csv'),
]

bvbrc_frames = []
for f in bvbrc_files:
    df = pd.read_csv(f, low_memory=False)
    country = os.path.basename(f).replace('BVBRC_','').replace('_Metadata.csv','')
    df['Source_Country'] = country
    bvbrc_frames.append(df)

bvbrc = pd.concat(bvbrc_frames, ignore_index=True)
print(f"BV-BRC total rows: {len(bvbrc)}")

# ── Step 2: Load NCBI metadata ────────────────────────────────
print("Loading NCBI metadata...")
ncbi = pd.read_csv(os.path.join(NCBI_DIR, 'NCBI_India_Metadata.csv'),
                   low_memory=False)
print(f"NCBI total rows: {len(ncbi)}")

# ── Step 3: Extract GCA accessions from BV-BRC ───────────────
print("\nExtracting GCA accessions from BV-BRC...")

# BV-BRC stores accession in 'Assembly Accession' column
# Format: GCA_XXXXXXXXX.V
bvbrc_accessions = bvbrc['Assembly Accession'].dropna().astype(str).str.strip()

def classify_accession(acc):
    """
    Classify an accession number as GCA (valid) or WGS (excluded).

    GCA format: GCA_XXXXXXXXX.V
    WGS/JAGIMY format: starts with letters like JAGIMY, SAMN, etc.
    """
    acc = str(acc).strip()
    if re.match(r'^GCA_\d+\.\d+$', acc):
        return 'GCA'
    elif acc.startswith('GCA') and not re.match(r'^GCA_\d+\.\d+$', acc):
        return 'GCA_malformed'
    else:
        return 'WGS'

bvbrc['accession_type'] = bvbrc['Assembly Accession'].apply(
    lambda x: classify_accession(x) if pd.notna(x) else 'missing'
)

# Count each type
type_counts = bvbrc['accession_type'].value_counts()
print(f"\nBV-BRC accession types:")
print(type_counts)

# ── Step 4: Extract GCA accessions from NCBI ─────────────────
print("\nExtracting GCA accessions from NCBI...")
ncbi_accessions = ncbi['Assembly Accession'].dropna().astype(str).str.strip()
ncbi_gca = ncbi_accessions[
    ncbi_accessions.apply(lambda x: bool(re.match(r'^GCA_\d+\.\d+$', x)))
].tolist()
print(f"NCBI valid GCA accessions: {len(ncbi_gca)}")

# ── Step 5: Combine and deduplicate ──────────────────────────
print("\nCombining and deduplicating...")

# Valid BV-BRC GCAs
bvbrc_gca = bvbrc[bvbrc['accession_type'] == 'GCA']['Assembly Accession']\
    .astype(str).str.strip().tolist()

# WGS accessions (excluded)
bvbrc_wgs = bvbrc[bvbrc['accession_type'] == 'WGS']['Assembly Accession']\
    .dropna().astype(str).str.strip().tolist()

# Missing accessions
bvbrc_missing = bvbrc[bvbrc['accession_type'] == 'missing'].shape[0]

# Combine BV-BRC GCA + NCBI GCA, remove duplicates
all_gca = list(set(bvbrc_gca + ncbi_gca))
all_gca.sort()  # sort for reproducibility

# All WGS format accessions
all_wgs = list(set(bvbrc_wgs))
all_wgs.sort()

print(f"\nSummary:")
print(f"  Valid GCA accessions (BV-BRC + NCBI, deduplicated): {len(all_gca)}")
print(f"  WGS format accessions (excluded): {len(all_wgs)}")
print(f"  Missing accession numbers: {bvbrc_missing}")
print(f"  Total BV-BRC rows: {len(bvbrc)}")

# ── Step 6: Filter for human clinical isolates ───────────────
print("\nFiltering for human clinical isolates...")

# Re-filter BV-BRC for human hosts only
bvbrc_human = bvbrc[
    bvbrc['Host Name'].str.contains('human|Human|Homo', na=False)
]['Assembly Accession'].dropna().astype(str).str.strip()

bvbrc_human_gca = bvbrc_human[
    bvbrc_human.apply(lambda x: bool(re.match(r'^GCA_\d+\.\d+$', x)))
].tolist()

# NCBI metadata for India — all clinical
ncbi_human_gca = ncbi_gca.copy()

# Combined human clinical GCAs
final_gca = list(set(bvbrc_human_gca + ncbi_human_gca))
final_gca.sort()

print(f"  Human clinical GCA accessions: {len(final_gca)}")

# ── Step 7: Write accession files ────────────────────────────
print("\nWriting accession files...")

# Main accession list
with open(os.path.join(OUTPUT_DIR, 'gca_accessions_final.txt'), 'w') as f:
    for acc in final_gca:
        f.write(acc + '\n')
print(f"  Written: gca_accessions_final.txt ({len(final_gca)} accessions)")

# WGS excluded accessions
with open(os.path.join(OUTPUT_DIR, 'wgs_accessions.txt'), 'w') as f:
    for acc in all_wgs:
        f.write(acc + '\n')
print(f"  Written: wgs_accessions.txt ({len(all_wgs)} accessions)")

# Split into 4 batches for download
# NCBI Datasets CLI works best with batches of ~75 accessions
batch_size = math.ceil(len(final_gca) / 4)
for i in range(4):
    batch = final_gca[i * batch_size : (i + 1) * batch_size]
    batch_file = os.path.join(OUTPUT_DIR, f'batch{i+1}.txt')
    with open(batch_file, 'w') as f:
        for acc in batch:
            f.write(acc + '\n')
    print(f"  Written: batch{i+1}.txt ({len(batch)} accessions)")

# ── Step 8: Print final summary ──────────────────────────────
print("\n" + "="*60)
print("ACCESSION LIST BUILDING COMPLETE")
print("="*60)
print(f"Total valid GCA accessions:     {len(final_gca)}")
print(f"WGS excluded accessions:        {len(all_wgs)}")
print(f"Missing accession numbers:      {bvbrc_missing}")
print(f"Batches created:                4")
print(f"\nOutput files in: {OUTPUT_DIR}/")
print(f"  gca_accessions_final.txt")
print(f"  wgs_accessions.txt")
print(f"  batch1.txt to batch4.txt")
print(f"\nNext step: Run scripts/01_download_genomes.sh")
print("="*60)
