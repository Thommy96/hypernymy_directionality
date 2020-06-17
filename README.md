# Hypernymy Directionality
Data and code for the experiments in: Bachelor Thesis Thomas Bott

## Usage notes
The scripts should be run directy from their directory with python3. Each script contains a usage pattern, which indicates how to use it. Further information about the arguments and options can be obtained with the -h (--help) option.
For successfull usage, it is recommended to execute the scripts in the following order:
1. Create distributional semantic space(s) (scripts/dsm_creation/)
  > - dsm_creation.py 
  > - dsm_combine.py
2. Calculate row sums (scripts/dsm_creation/)
  > - rowSums.py
3. Read data set(s) (scripts/dataset_processing/)
  > -   read_dataset.py
4. Filter data set(s) (scripts/dataset_processing/)
  > - filter_dataset.py
5. Optionally create subsets of data set(s) (scripts/dataset_processing/)
  > - slices_freqBias.py
6. For SLQS, calculate Positive Local Mutual Information scores (scripts/dsm_creation/)
  > - plmi.py
7. Calculate unsupervised hypernymy measures (scripts/measures/)
 > - weedsPrec.py
 > - invCL.py
 > - slqsRow.py
 > - slqs.py
 8. Evaluate measures, unsupervised and supervised (scripts/evaluation/)
  > - evaluation.py
  > - classification.py

## Test corpora
For testing purposes, the two test corpora in materials/corpora/ can be used.
They are smaller parts of the original SdeWaC and PukWaC copora and allow to test the code with a short runtime.
