# Alzheimer's Disease (AD) Prediction
### CSE 283
### Group Members: Kate Jackson, Safa Saeed, Jonah Silverman

# Dataset
We combined blood extracellular RNA sequencing data from three different cohorts:
* [SILVER-seq](https://github.com/Zhong-Lab-UCSD/AD_prediction_blood/tree/main/silver_seq): 115 samples total, 41 normal from 9 donors and 74 AD from 15 donors
* [Toden et al.](https://github.com/Zhong-Lab-UCSD/AD_prediction_blood/tree/main/toden): 334 samples total, 164 normal from 114 donors and 170 AD from 126 donors
* [Burgos et al.](https://github.com/Zhong-Lab-UCSD/AD_prediction_blood/tree/main/burgos_dbgap): 267 samples total, 138 normal from 74 donors and 129 AD from 70 donors

The common metadata information we found in all three datasets included sex, age, AD diagnosis, and APOE status, which we used as features for our classification model.

# Classification Methods
We implemented three classical machine learning methods using [scikit-learn](https://scikit-learn.org/stable/): random forest (RF), naive Bayes (NB), and logistic regression (LR). We also utilized the multilayer perceptron from [skorch](https://skorch.readthedocs.io/en/stable/).

For each of the four models, we evaluated multiple combinations of data partitioning and feature selection. Namely, we first combined all three datasets into one group that was used for training, testing, and cross-validation. We also trained and validated on two datasets combined, and held out the third dataset for testing. Our metadata features consisted of sex, age, and APOE status when available. We added relevant gene features based on differential expression using [PyDESeq2](https://pydeseq2.readthedocs.io/en/stable/) and weighted gene co-expression analysis using [WGCNA](https://pmc.ncbi.nlm.nih.gov/articles/PMC2631488/).

# Results
Overall, the RF classifier trained on metadata with APOE genotypes alone achieved the optimal performance on the combined datasets, with an AUC of 0.781. In contrast, the NB classifier trained on metadata with APOE genotypes alone achieved the optimal performance when each dataset was held out, with an average AUC of 0.648. Complete results can be viewed in our [final project report](https://docs.google.com/document/d/1tj5yBhHQY3J-M9Jo8MSwrcCFQiKh5ecZq7VSo0cMIgM/edit?usp=sharing).

# Sources

- https://bioinformaticsworkbook.org/tutorials/wgcna.html
- https://smorabit.github.io/hdWGCNA/articles/module_preservation.html
