# Code Examples

### This repository contains an assortment of code examples and mini-extracts from larger projects.

### File descriptions:
-------------------------

| **SN** |  **File**   | **Description** |
|----------------|------------|------------|
|1|[Example_of_Database_Driven_Analysis.R](https://github.com/rasiimwe/Code_Examples/blob/main/Example_of_Database_Driven_Analysis.R)|This file provides an example on how to conduct database_driven analyses in R and produces the following [multi-hit oncoplot](https://github.com/rasiimwe/Code_Examples/blob/main/oncoplot_funccall.pdf)|
|2|[Breat_cancer_prediction.ipynb](https://github.com/rasiimwe/Code_Examples/blob/main/Predicting_Breast_Cancer_Using_Machine_Learning.ipynb)|Using the [Wisconsin breast cancer diagnostic dataset](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+%28Diagnostic%29) for predictive analysis using *Jupyter Notebook, Python - numpy, pandas, matplotlib, seaborn, scikit-learn*. This was one of my rookie machine learning projects|
|3|[Genomic_Subgroups.py](https://github.com/rasiimwe/Code_Examples/blob/main/Genomic_Subgroups.py)|Application of [Dash-Python](https://dash.plotly.com) in visualizing genomic data. Dash is written on top of powerful libraries and frameworks such as Flask, Plotly.js, and React.js|
|4|[Mutation_loads.py](https://github.com/rasiimwe/Code_Examples/blob/main/Mutation_loads.py)|This file also contains an extract from a larger project on using Dash-Python to create interactive interfaces for visualizing big and complex datasets from back end databases and systems. Please refer to the file for key libraries implemented|
|5|[Mutations_ETL.R](https://github.com/rasiimwe/Code_Examples/blob/main/Mutations_ETL.R)|Most of the data I have worked with was extracted from variant callers (tools/software used to detect variants from sequencing data) that store their data in vcf or text files. The [structure](https://github.com/rasiimwe/Code_Examples/blob/main/VCF_Extract.png) of these large files is complex (largely unstructured), data values are not atomic, and the data is not linked to other data components required for integrated data analysis, which hinders effective and efficient data mining processes. This file contains an example of code used to navigate through server files for specific files of interest, reads the data from each called file, structures or transforms the data and finally bulk-loads the clean and structured data into a backend database (an object-relational PostgreSQL database). Each file contains thousands of mutations per line, culminating into millions of records in the database (database constraints like key constraints and referential integrity were further defined between objects). I spent a considerable amount of time optimizing the database to reduce the runtime. It paid off!!. Processes that took hours, like searching and integrating data for downstream analysis, now only took a minute or two! This also aided analyses of orthogonally collected data in ways we hadn't seen before!|
|6|[Mutations_ETL2.py](https://github.com/rasiimwe/Code_Examples/blob/main/Mutations_ETL2.py)|This file contains another example on data extraction, transformation and loading implemented in Python|
|7|[Pipeline_result_paths.py](https://github.com/rasiimwe/Code_Examples/blob/main/Pipeline_result_paths.py)|Example 2 on python-based ETL|
|8|[Samples_Object.py](https://github.com/rasiimwe/Code_Examples/blob/main/Samples_Object.py)|This file contains code that opens a connection to the backend database (also implemented in most files), creates required database objects and loads structured data into the created database object - a more efficient  way of creating database objects and loading data at the same time|
|9|[WGS_QC.py](https://github.com/rasiimwe/Code_Examples/blob/main/WGS_QC.py)|This file contains a Dash example on quality control checks and visualization of sequencing data|
|10|[DNAme preprocessing.Rmd](https://github.com/rasiimwe/Code_Examples/blob/main/DNAme%20preprocessing.Rmd)|This file contains examples of key steps required to preprocess DNA methylation data from raw IDAT files|
|11|[Linear_Mixed_Effects_Models.Rmd](https://github.com/rasiimwe/Code_Examples/blob/main/Linear_Mixed_Effects_Models.Rmd)|This file contains an example on fitting linear mixed-effects model (LMMs) using lmer on over 5000 CpG sites to investigate the association between DNA methylation and disease given various exposures|
|12|[ExtendedFigs_NatMed.pdf](https://github.com/rasiimwe/Code_Examples/blob/main/ExtendedFigs_NatMed.pdf)|This file encapsulates examples of single-cell RNA seq and spatial transcriptomics analyses conducted in preparation of the manuscript: [Spatiotemporal immune atlas of the first clinical-grade,gene-edited pig-to-human kidney xenotransplant](https://www.researchsquare.com/article/rs-2382345/v1). Towards publication, I have also compiled and posted key analyses that I conducted during the generation of this manuscript - accessible on this [github page](https://github.com/PorrettLab/Spatiotemporal-immune-atlas-of-the-1st-clinical-grade-gene-edited-pig-to-human-kidney-xenotransplant/tree/main) for your reference|
|13|[Image processing using Neural Networks and Convolutional Neural Networks.ipynb](https://github.com/rasiimwe/Code_Examples/blob/main/Image_processing_using_Neural_Networks_and_Convolutional_Neural_Networks.ipynb)|Using Artificial or Fully Connected Feed Forward Neural Networks and Convolutional Neural Networks to predict numbers within images|
|14|[Malarial Detection Using Deep Learning: A Convolutional Neural Networks (CNN) Approach.ipynb](https://github.com/rasiimwe/Code_Examples/blob/main/Malarial_Detection_Using_Deep_Learning_A_Convolutional_Neural_Networks_(CNN)_Approach.ipynb)|This notebook is on building automated and efficient computer vision models to detect malaria by distinguishing malaria parasitized red blood cells from uninfected red blood cells, and to classify which cells are parasitized - that is cells that have the Plasmodium parasite - and which cells are not (uninfected), in the midst of other cellular impurities|








