# Step-by-Step Database Download Guide

This guide documents exactly how the raw metadata and reference files were obtained for this study. All downloads are manual — no API or command line required for this step.

---

## Step 1 — Download from BV-BRC (Bacterial and Viral Bioinformatics Resource Center)

**What is BV-BRC?**
BV-BRC (https://www.bv-brc.org) is a US government-funded bacterial genomics database. It contains genome sequences and metadata for hundreds of thousands of bacterial isolates. It is the largest publicly available bacterial genomics database.

**What we downloaded:**
For each of four countries (India, Pakistan, Bangladesh, Nepal) we downloaded three CSV files:
- Metadata — genome accessions, collection year, isolation country, host, MLST
- AMR Phenotypes — phenotypic antibiotic resistance data
- Specialty Genes — resistance and virulence gene annotations

**How to download (repeat for each country):**

1. Go to https://www.bv-brc.org
2. Click **Organisms** in the top menu → **Bacteria**
3. Search for **Pseudomonas aeruginosa**
4. Click on **Pseudomonas aeruginosa** in the results
5. Click **Genomes** in the left panel
6. In the filter panel on the right, filter by:
   - **Isolation Country** = India (or Pakistan / Bangladesh / Nepal)
   - **Host Name** = Homo sapiens (human)
7. Select all results (click checkbox at top)
8. Click the **Download** button
9. Select **Metadata** → CSV format → Download
   - Save as: BVBRC_India_Metadata.csv
10. Repeat download for **AMR Phenotypes** → CSV
    - Save as: BVBRC_India_AMRPhenotypes.csv
11. Repeat download for **Specialty Genes** → CSV
    - Save as: BVBRC_India_SpecialtyGenes.csv
12. Repeat all steps for Pakistan, Bangladesh, Nepal

**Files produced (12 total):**
- BVBRC_India_Metadata.csv
- BVBRC_India_AMRPhenotypes.csv
- BVBRC_India_SpecialtyGenes.csv
- BVBRC_Pakistan_Metadata.csv
- BVBRC_Pakistan_AMRPhenotypes.csv
- BVBRC_Pakistan_SpecialtyGenes.csv
- BVBRC_Bangladesh_Metadata.csv
- BVBRC_Bangladesh_AMRPhenotypes.csv
- BVBRC_Bangladesh_SpecialtyGenes.csv
- BVBRC_Nepal_Metadata.csv
- BVBRC_Nepal_AMRPhenotypes.csv
- BVBRC_Nepal_SpecialtyGenes.csv

All files are stored in: data/metadata/bvbrc/

---

## Step 2 — Download from NCBI (National Center for Biotechnology Information)

**What is NCBI?**
NCBI (https://www.ncbi.nlm.nih.gov) is the primary US government genomic repository. All genome sequences published in research papers are deposited here.

**Why NCBI in addition to BV-BRC?**
BV-BRC does not always have the most recent genome submissions. We downloaded additional Indian P. aeruginosa genomes from NCBI specifically for collection years 2018-2024 to ensure recent genomes were included.

**How to download:**

1. Go to https://www.ncbi.nlm.nih.gov/datasets/genome/
2. Search for: **Pseudomonas aeruginosa**
3. Filter by:
   - **Assembly level** = Complete or Chromosome or Scaffold or Contig
   - **Source database** = GenBank
4. Click **Download** → **Metadata only** → CSV format
5. Save as: NCBI_India_Metadata.csv

**File produced:**
- NCBI_India_Metadata.csv

Stored in: data/metadata/ncbi/

---

## Step 3 — Download from PubMLST

**What is PubMLST?**
PubMLST (https://pubmlst.org) is a curated database for Multi-Locus Sequence Typing (MLST) data. It contains thousands of P. aeruginosa isolates with their allele profiles and assigned Sequence Type (ST) numbers.

**Important note:** PubMLST data was used as reference only for building the ST-to-CC (Clonal Complex) mapping dictionary. It could NOT be merged with the genomic data because PubMLST uses internal lab IDs (e.g. 2073/12) that cannot be matched to GCA accession numbers.

**How to download:**

1. Go to https://pubmlst.org/organisms/pseudomonas-aeruginosa
2. Click **Isolates** → **Search isolates**
3. Filter by **Country** = India (repeat for Pakistan, Bangladesh, Nepal)
4. Select all results
5. Click **Download** → Excel format
6. Save as: PubMLST_India.xlsx

**Files produced (4 total):**
- PubMLST_India.xlsx
- PubMLST_Pakistan.xlsx
- PubMLST_Bangladesh.xlsx
- PubMLST_Nepal.xlsx

Stored in: data/metadata/pubmlst/

---

## Summary

| Database | Files | Purpose |
|----------|-------|---------|
| BV-BRC | 12 CSV files | Primary metadata source — country, year, MLST, host |
| NCBI | 1 CSV file | Supplementary Indian genomes 2018-2024 |
| PubMLST | 4 XLSX files | ST-to-CC reference mapping only |
| **Total** | **17 files** | All stored in data/metadata/ |

---

## Next Step

After downloading all files, proceed to:
**scripts/00_build_accession_list.py** — filters metadata and builds the GCA accession list for genome download.
