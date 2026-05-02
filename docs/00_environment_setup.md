# Environment Setup Guide — From Zero

This guide documents every software installation step required to reproduce this analysis, starting from a Windows laptop with nothing installed.

---

## System Used in This Study

- **Laptop:** ASUS Vivobook 16x
- **OS:** Windows 10/11
- **RAM:** 16 GB
- **Storage:** Sufficient free space (~10 GB recommended)

---

## Step 1 — Install Ubuntu WSL2 on Windows

WSL2 (Windows Subsystem for Linux 2) allows running Ubuntu Linux on a Windows machine. StarAMR requires Linux to run.

**Why WSL2?**
StarAMR and its dependencies (BLAST, MLST, Perl modules) are designed for Linux. They cannot run natively on Windows.

**Installation:**

1. Open PowerShell as Administrator
2. Run:
3. Restart your computer when prompted
4. Ubuntu will open automatically after restart
5. Create a username and password when prompted

**Verify installation:**
```bash
lsb_release -a
# Should show: Ubuntu 22.04.x LTS
```

---

## Step 2 — Install Anaconda (conda)

Conda is a package and environment manager. We use it to create an isolated environment for StarAMR.

**Why conda?**
StarAMR requires specific versions of BLAST, MLST, and Perl. Installing them in an isolated conda environment prevents version conflicts with other software.

**Installation:**

1. Open Ubuntu terminal
2. Download Anaconda installer:
```bash
wget https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh
```
3. Run installer:
```bash
bash Anaconda3-2023.09-0-Linux-x86_64.sh
```
4. Follow prompts, accept license, confirm install location
5. Type yes when asked to initialize conda
6. Close and reopen terminal
7. Verify:
```bash
conda --version
```

---

## Step 3 — Create StarAMR Environment and Install StarAMR

```bash
# Create dedicated environment
conda create -n staramr_env -c conda-forge -c bioconda staramr

# Activate environment
conda activate staramr_env

# Verify versions
staramr --version
# Expected: staramr 0.12.1

blastn -version
# Expected: blastn: 2.16.0

mlst --version
# Expected: mlst 2.32.2

perl --version
# Expected: perl 5.32.1
```

**Software versions used in this study:**
| Software | Version |
|----------|---------|
| StarAMR | 0.12.1 |
| BLAST | 2.16.0 |
| MLST | 2.32.2 |
| Perl | 5.32.1 |
| Ubuntu | 22.04.5 LTS |

---

## Step 4 — Install NCBI Datasets CLI Tool on Windows

The NCBI Datasets CLI (Command Line Interface) tool is used to download FASTA genome files from NCBI. It runs on Windows — NOT inside Ubuntu.

**Why Windows and not Ubuntu?**
The FASTA files are large (~1.7 GB total). Downloading to Windows gives direct access via File Explorer without path translation.

**Installation:**

1. Go to: https://www.ncbi.nlm.nih.gov/datasets/docs/v2/download-and-install/
2. Download the **Windows** version (datasets.exe)
3. Save it to a convenient location, e.g. C:\Users\YourName\Downloads\
4. Open Command Prompt (not PowerShell, not Ubuntu)
5. Navigate to the folder:
6. Verify:
---

## Step 5 — Set Up Kaggle for Python Analysis

All Python analysis is performed on Kaggle — a free cloud computing platform. No local Python installation is required.

**Why Kaggle?**
- Free cloud computing (no GPU needed for this project)
- Pre-installed scientific Python libraries (pandas, matplotlib, seaborn, numpy, scipy)
- Datasets can be uploaded and shared publicly
- Jupyter notebook format ensures reproducibility

**Setup:**

1. Go to https://www.kaggle.com
2. Create a free account
3. Click your profile picture → **Settings** → **Phone Verification** (required for internet access in notebooks)
4. Verify your phone number
5. Create two datasets (see scripts/00_build_accession_list.py for what files to upload)
6. Create a new notebook and add both datasets as inputs

---

## Summary

| Step | Tool | Platform | Purpose |
|------|------|----------|---------|
| 1 | Ubuntu WSL2 | Windows | Linux environment for StarAMR |
| 2 | Anaconda (conda) | Ubuntu | Package management |
| 3 | StarAMR v0.12.1 | Ubuntu (conda) | ARG detection |
| 4 | NCBI Datasets CLI | Windows | FASTA download |
| 5 | Kaggle | Web browser | Python analysis |

---

## Next Step

After environment setup proceed to:
**docs/01_database_download_guide.md** — manually download metadata from BV-BRC, NCBI, PubMLST.
