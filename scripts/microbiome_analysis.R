# ==========================================================
# Project:
# Multi-Omics Characterization of the Oral–Gut–Brain Axis
# in Parkinson's Disease
#
# Description:
# R workflow for microbiome diversity analysis, differential
# abundance analysis, Oral Enrichment Score (OES)
# calculation, and machine learning dataset preparation.
#
# Author: Praveen Kumar S
# Year: 2026
# ==========================================================


library(vegan)
library(readxl)
library(ggplot2)

# Load species matrix
data <- read.table(
  "species_abundance_matrix.tsv",
  header=TRUE,
  row.names=1,
  sep="\t",
  check.names=FALSE
)

# Replace NA
data[is.na(data)] <- 0

# Transpose
data_t <- t(data)

# Load metadata
metadata <- read_excel("metadata_final.xlsx")

metadata <- metadata[
  match(rownames(data_t),
        metadata$Run),
]


shannon <- diversity(
  data_t,
  index="shannon"
)

simpson <- diversity(
  data_t,
  index="simpson"
)

diversity_df <- data.frame(
  Sample = rownames(data_t),
  Shannon = shannon,
  Simpson = simpson,
  Group = metadata$Group
)

write.table(
  diversity_df,
  "alpha_diversity_results.tsv",
  sep="\t",
  row.names=FALSE
)

ggplot(
  diversity_df,
  aes(Group, Shannon, fill=Group)
) +
  geom_boxplot() +
  theme_bw()  


bray_dist <- vegdist(
  data_t,
  method="bray"
)

pcoa <- cmdscale(
  bray_dist,
  k=2
)

pcoa_df <- data.frame(
  Sample = rownames(pcoa),
  PC1 = pcoa[,1],
  PC2 = pcoa[,2],
  Group = metadata$Group
)

ggplot(
  pcoa_df,
  aes(PC1, PC2, color=Group)
)+
  geom_point(size=3)+
  theme_bw()

adonis2(
  bray_dist ~ Group,
  data = metadata,
  permutations = 999
)


library(DESeq2)

count_data <- round(data)

count_data <- count_data[
  rowSums(count_data) > 10,
]

metadata_deseq <- metadata[
  match(colnames(count_data),
        metadata$Run),
]

metadata_deseq$Group <- factor(
  metadata_deseq$Group
)

dds <- DESeqDataSetFromMatrix(
  countData = count_data,
  colData = metadata_deseq,
  design = ~ Group
)

dds <- estimateSizeFactors(
  dds,
  type="poscounts"
)

dds <- DESeq(dds)

res_PD_vs_HC <- results(
  dds,
  contrast=c("Group","PD","HC")
)

sig_species <- res_PD_vs_HC[
  which(res_PD_vs_HC$padj < 0.05),
]

write.csv(
  sig_species,
  "PD_vs_HC_significant_species.csv"
)

homd <- read_excel(
  "HOMD_oral.xlsx",
  skip=1
)

homd_species <- paste(
  homd$Genus,
  homd$Species
)

project_species <- rownames(sig_species)

oral_overlap <- project_species[
  project_species %in% homd_species
]

length(oral_overlap)


oral_subset <- count_data[
  rownames(count_data) %in%
    oral_overlap,
]

oral_counts <- colSums(
  oral_subset
)

total_counts <- colSums(
  count_data
)

OES <- oral_counts / total_counts

OES_df <- data.frame(
  Sample = names(OES),
  OES = OES
)

OES_df$Group <- metadata_deseq$Group

write.csv(
  OES_df,
  "OES_scores.csv"
)

rel_abundance <- sweep(
  count_data,
  2,
  colSums(count_data),
  "/"
)

top50 <- sig_species[
  order(sig_species$padj),
][1:50, ]

top_species_names <- rownames(top50)

top_species_data <- t(
  rel_abundance[
    top_species_names,
  ]
)

top_species_data <- as.data.frame(
  top_species_data
)

top_species_data$OES <- OES_df$OES
top_species_data$Shannon <- diversity_df$Shannon
top_species_data$Simpson <- diversity_df$Simpson

top_species_data$Group <- ifelse(
  metadata_deseq$Group=="HC",
  "HC",
  "PD"
)

write.csv(
  top_species_data,
  "ML_dataset_proper.csv",
  row.names=FALSE
)

