```markdown
# Multi-Omics Characterization of the Oral-Gut-Brain Axis in Parkinson's Disease

## Overview

This repository contains the source code, analysis workflow, and supporting files for my Master's thesis submitted in partial fulfillment of the Master of Science (M.Sc.) in Bioinformatics at REVA University.

The project investigates the role of the **Oral–Gut–Brain Axis** in **Parkinson's Disease (PD)** using **shotgun metagenomics**, **functional microbiome analysis**, and **machine learning** to identify microbial translocation signatures and predictive biomarkers.

---

## Project Title

**Multi-Omics Characterization of the Oral-Gut-Brain Axis in Parkinson's Disease: Identification of Microbial Translocation Signatures and Biomarkers**

---

## Research Objectives

- Investigate oral and gut microbial dysbiosis associated with Parkinson's Disease.
- Identify oral-to-gut microbial translocation signatures.
- Characterize microbial functional pathways and virulence factors.
- Develop machine learning models for Parkinson's disease prediction.
- Discover microbial biomarkers associated with disease progression.

---

## Dataset

**Project ID:** PRJEB79944

Source:
- NCBI Sequence Read Archive (SRA)

Samples Included:

| Clinical Group | Samples |
|---------------|---------|
| Healthy Controls (HC) | 52 |
| Parkinson's Disease (PD) | 20 |
| PD with Mild Cognitive Impairment (PD-MCI) | 78 |
| Parkinson's Disease Dementia (PDD) | 91 |

**Total Samples:** 241

---

## Workflow

```
<img width="1088" height="754" alt="image" src="https://github.com/user-attachments/assets/3d384a7f-6277-47c8-b1c0-ba926d2ee901" />
                Public Shotgun Metagenomic Dataset
                           (PRJEB79944)
                                   │
                                   ▼
                  Internal Preprocessing Pipeline*
                                   │
        (*Not included due to confidentiality restrictions)
                                   │
                                   ▼
                     Species Abundance Matrix
                                   │
                ┌──────────────────┴──────────────────┐
                ▼                                     ▼
        R Microbiome Analysis                 Machine Learning
                │                                     │
      • Alpha Diversity                      • Feature Engineering
      • Beta Diversity                       • SMOTE
      • DESeq2                               • XGBoost
      • Oral Enrichment Score                • Random Forest
      • Differential Abundance               • Cross Validation
                │                                     │
                └──────────────┬──────────────────────┘
                               ▼
                   Biomarker Identification
                               │
                               ▼
                 Virulence & MetaCyc Annotation
                               │
                               ▼
                 Integrated Mechanistic Network
                               │
                               ▼
                  Parkinson's Disease Biomarkers

```

---

## Bioinformatics Tools

### Quality Control

- FastQC
- MultiQC
- fastp
- KneadData
- FastQ Screen

### Taxonomic Profiling

- Kraken2
- Bracken
- Krona

### Functional Analysis

- MetaCyc
- VFDB

### Programming

- Python
- R

### Machine Learning

- XGBoost
- Random Forest
- SMOTE
- SHAP

### Visualization

- Matplotlib
- Seaborn
- PyVis

---

## Machine Learning Pipeline

Features used:

- Species abundance
- Alpha diversity
- Beta diversity
- Oral Enrichment Score (OES)
- Functional pathways
- Virulence signatures

Models:

- Random Forest
- XGBoost

Evaluation Metrics:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC
- PR-AUC

---

## Key Findings

- Oral microbial dysbiosis increases with Parkinson's disease progression.
- Elevated Oral Enrichment Score suggests oral-to-gut microbial translocation.
- Functional pathway alterations indicate increased inflammatory activity.
- Virulence factor enrichment supports microbial involvement in neurodegeneration.
- XGBoost demonstrated excellent predictive performance for Parkinson's disease classification.
- Multiple microbial biomarkers associated with disease progression were identified.

---

## Repository Structure

```

├── data/
│   ├── metadata/
│   ├── processed/
│   └── abundance_tables/
│
├── scripts/
│   ├── preprocessing/
│   ├── taxonomy/
│   ├── diversity/
│   ├── machine_learning/
│   ├── functional_analysis/
│   └── visualization/
│
├── notebooks/
│
├── figures/
│
├── results/
│
├── docs/
│
├── README.md
├── requirements.txt
└── LICENSE

```

---

## Requirements

Python packages

```

pandas
numpy
scikit-learn
xgboost
imbalanced-learn
matplotlib
seaborn
biopython
networkx
pyvis

```

R packages

```

phyloseq
vegan
ggplot2
DESeq2
tidyverse

```

---

## Citation

If you use this repository in your research, please cite:

Praveen Kumar S.

**Multi-Omics Characterization of the Oral-Gut-Brain Axis in Parkinson's Disease: Identification of Microbial Translocation Signatures and Biomarkers.**

Master's Thesis

REVA University

2026

---

## Author

**Praveen Kumar S**

M.Sc. Bioinformatics

REVA University

Bengaluru, India

GitHub: https://github.com/Praveen26-09

---

## License

This project is released under the MIT License.
```
