# PAeruginosa-AMR-SouthAsia

## Analysis of Emerging Antimicrobial Resistance Genes Using Publicly Available *Pseudomonas aeruginosa* Genomes

**Author:** Y. Lakshmi Sai Varshini, Saloni Semwal
**Institution:** SRM Institute of Science and Technology, Department of Genetic Engineering
**Supervisor:** Dr. P. Rathinasabapathi
**Program:** B.Tech. in Biotechnology (Computational Biology) — 3rd Year Minor Project

---

## Project Overview

Fully reproducible bioinformatics pipeline for identification and analysis of acquired antimicrobial resistance genes (ARGs) in clinical *Pseudomonas aeruginosa* isolates from South Asia (India, Pakistan, Bangladesh, Nepal) using publicly available whole genome sequences. Entirely computational — no wet lab work performed.

---

## Key Results

- 281 whole genome assemblies analysed
- 201/281 (71.5%) genomes carry at least one acquired ARG
- 1549 total acquired ARG detections
- 94 unique acquired ARGs identified
- Most prevalent: sul1 (67.6%), tet(G) (34.9%), CmlA9 (34.2%)
- Clinically critical: blaNDM-1 (12.5%), rmtF (19.3%), qnrVC1 (11.1%)
- Emerging ARGs: rmtF and qnrVC1 — both appear exclusively from 2010 onwards

---

## Repository Structure

    PAeruginosa-AMR-SouthAsia/
    data/
        accessions/
            gca_accessions_final.txt     — 281 GCA accessions used in analysis
            wgs_accessions.txt           — 71 WGS accessions excluded
            batch1.txt to batch4.txt     — NCBI download batch lists
        metadata/
            bvbrc/                       — BV-BRC CSV files (4 countries)
            ncbi/                        — NCBI supplementary metadata
            pubmlst/                     — PubMLST ST/CC reference XLSX files
    results/
        staramr/                         — StarAMR v0.12.1 output files
        figures/final/                   — 5 final publication figures
    scripts/                             — Analysis notebook (Kaggle)
    docs/                                — Methodology documentation

---

## How to Reproduce

### Step 1 — Download FASTA files
Use accession list in data/accessions/gca_accessions_final.txt with NCBI Datasets CLI:
    datasets download genome accession --inputfile gca_accessions_final.txt

### Step 2 — Run StarAMR
    conda create -n staramr_env -c conda-forge -c bioconda staramr
    conda activate staramr_env
    staramr search --output-dir staramr_output $(find ./fasta_all -name "*.fna")

### Step 3 — Run Python analysis
Open scripts/analysis.ipynb in Kaggle or Jupyter.
Upload staramr output and metadata files as datasets.

---

## Software Versions

- StarAMR: v0.12.1
- BLAST: 2.16.0
- MLST: 2.32.2
- Python: 3.12
- pandas, matplotlib, seaborn, numpy, scipy
- OS: Ubuntu 22.04.5 WSL2

---

## Data Sources

- BV-BRC: https://www.bv-brc.org
- NCBI Datasets: https://www.ncbi.nlm.nih.gov/datasets
- PubMLST: https://pubmlst.org/organisms/pseudomonas-aeruginosa
- ResFinder database: https://cge.food.dtu.dk/services/ResFinder
